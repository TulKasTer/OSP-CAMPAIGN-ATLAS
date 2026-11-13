"""Orchestration service for 2-phase Campaign coding and Aggregate Report coding."""

from __future__ import annotations

from ..prompts import (
    CAMPAIGN_FULL_CODING_SYSTEM_PROMPT,
    CAMPAIGN_GATES_SYSTEM_PROMPT,
    REPORT_CODING_SYSTEM_PROMPT,
    build_campaign_full_coding_user_prompt,
    build_campaign_gates_user_prompt,
    build_report_coding_user_prompt,
)
from ..schemas.api import (
    CodeCampaignRequest,
    CodeCampaignResponse,
    CodeReportRequest,
    CodeReportResponse,
    EvaluateGatesRequest,
    EvaluateGatesResponse,
)
from ..schemas.campaign import (
    CampaignGatesEvaluation,
    CampaignLLMExtraction,
    CampaignRecord,
    ExclusionLogRecord,
)
from ..schemas.common import (
    DEFAULT_AGREEMENT_RATE,
    NOT_SPECIFIED_REPORT,
    SourceMetadata,
    current_utc_zulu,
    derive_publisher_type,
)
from ..schemas.report import ReportLLMExtraction, ReportRecord
from .llm_client import StructuredLLMClient
from .scraper import fetch_url_content_and_metadata
from .storage import AtlasStorageService


class AtlasCodingService:
    """Service implementing the CODING ORDER V1.0 and FREEZE CODING SCHEME V2.1 workflows."""

    def __init__(self, llm_client: StructuredLLMClient | None = None) -> None:
        self.llm_client = llm_client or StructuredLLMClient()

    def _resolve_input_document(
        self,
        raw_text: str | None,
        url: str | None,
    ) -> tuple[str, SourceMetadata | None]:
        """Resolve text and source metadata from `raw_text` and/or `url`."""
        metadata: SourceMetadata | None = None
        if raw_text and raw_text.strip():
            return raw_text.strip(), metadata

        if not url or not url.strip():
            raise ValueError("Either 'raw_text' or 'url' must be provided.")

        fetched = fetch_url_content_and_metadata(url.strip())
        return fetched.extracted_text, fetched.metadata

    def evaluate_campaign_gates(self, request: EvaluateGatesRequest) -> EvaluateGatesResponse:
        """Stage 1: Evaluate Gates #1-#3 (Rule #1, Rule #2, Rule #3) and Target Identification."""
        text, metadata = self._resolve_input_document(request.raw_text, request.url)
        user_prompt = build_campaign_gates_user_prompt(
            text=text,
            url=request.url,
            metadata=metadata,
        )

        gates = self.llm_client.extract(
            response_model=CampaignGatesEvaluation,
            system_prompt=CAMPAIGN_GATES_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            override=request.llm_config,
            phase="gates",
        )

        exclusion_entry: ExclusionLogRecord | None = None
        saved_paths: list[str] = []

        if gates.is_excluded:
            excluded_id = request.excluded_id or AtlasStorageService.next_excluded_id()
            exclusion_entry = ExclusionLogRecord(
                excluded_id=excluded_id,
                campaign_name=gates.campaign_name,
                publisher=gates.publisher,
                information_website=request.url or (metadata.url if metadata else NOT_SPECIFIED_REPORT),
                rule_triggered=gates.rule_triggered or "Rule #1",
                exclusion_reason=gates.exclusion_reason or "Excluded under mandatory eligibility gates.",
                exclusion_date=current_utc_zulu(),
                evaluator=request.evaluator,
            )
            if request.save_to_disk:
                saved_paths = AtlasStorageService.save_exclusion_log(exclusion_entry)

        return EvaluateGatesResponse(
            status="excluded" if gates.is_excluded else "eligible",
            gates_evaluation=gates,
            exclusion_log_entry=exclusion_entry,
            source_metadata=metadata,
            saved_paths=saved_paths,
        )

    def code_campaign(self, request: CodeCampaignRequest) -> CodeCampaignResponse:
        """Execute 2-phase Campaign coding: Stage 1 (Gates #1-#3) -> Stage 2 (Phases 3-8 variables)."""
        text, metadata = self._resolve_input_document(request.raw_text, request.url)

        # Stage 1: Evaluate Eligibility Filters (Gates #1-#3)
        gates_prompt = build_campaign_gates_user_prompt(
            text=text,
            url=request.url,
            metadata=metadata,
        )
        gates = self.llm_client.extract(
            response_model=CampaignGatesEvaluation,
            system_prompt=CAMPAIGN_GATES_SYSTEM_PROMPT,
            user_prompt=gates_prompt,
            override=request.llm_config,
            phase="gates",
        )

        saved_paths: list[str] = []
        exclusion_entry: ExclusionLogRecord | None = None

        if gates.is_excluded:
            excluded_id = request.excluded_id or AtlasStorageService.next_excluded_id()
            exclusion_entry = ExclusionLogRecord(
                excluded_id=excluded_id,
                campaign_name=gates.campaign_name,
                publisher=gates.publisher,
                information_website=request.url or (metadata.url if metadata else NOT_SPECIFIED_REPORT),
                rule_triggered=gates.rule_triggered or "Rule #1",
                exclusion_reason=gates.exclusion_reason or "Excluded under mandatory eligibility gates.",
                exclusion_date=current_utc_zulu(),
                evaluator=request.evaluator,
            )
            if not request.force_full_coding:
                if request.save_to_disk:
                    saved_paths = AtlasStorageService.save_exclusion_log(exclusion_entry)
                return CodeCampaignResponse(
                    status="excluded",
                    gates_evaluation=gates,
                    campaign=None,
                    exclusion_log_entry=exclusion_entry,
                    source_metadata=metadata,
                    saved_paths=saved_paths,
                )

        # Stage 2: Extract remaining variables (Phases 3 to 8 of CODING ORDER V1.0)
        full_prompt = build_campaign_full_coding_user_prompt(
            text=text,
            gates=gates,
            url=request.url,
            metadata=metadata,
        )
        extracted = self.llm_client.extract(
            response_model=CampaignLLMExtraction,
            system_prompt=CAMPAIGN_FULL_CODING_SYSTEM_PROMPT,
            user_prompt=full_prompt,
            override=request.llm_config,
            phase="coding",
        )

        campaign_id = request.campaign_id or AtlasStorageService.next_campaign_id()
        publisher = extracted.publisher or gates.publisher or NOT_SPECIFIED_REPORT
        publisher_type = derive_publisher_type(publisher, fallback=extracted.publisher_type)

        # Enforce Registered Protocol V1 rule: mark inferred persuasion principles in note_on_ambiguity
        note = (extracted.note_on_ambiguity or "").strip()
        if extracted.persuasion_principles_inferred and "inferred" not in note.lower():
            inferred_suffix = "Persuasion principle(s): Inferred latently from explicit pretext/request text."
            note = f"{note} {inferred_suffix}".strip() if note and note.lower() != "none" else inferred_suffix

        info_website = (
            request.url
            or (metadata.url if metadata else None)
            or NOT_SPECIFIED_REPORT
        )

        campaign_record = CampaignRecord(
            campaign_id=campaign_id,
            campaign_name=extracted.campaign_name or gates.campaign_name,
            publisher=publisher,
            publisher_type=publisher_type,
            publication_date=extracted.publication_date or NOT_SPECIFIED_REPORT,
            case_source_type=gates.case_source_type,
            campaign_specificity=gates.campaign_specificity,
            attack_classification=gates.formatted_attack_classification(),
            targeting_evidence=gates.targeting_evidence,
            outcome=extracted.outcome,
            target=gates.target,
            channels=extracted.channels,
            channel_transition=extracted.channel_transition,
            tactics=extracted.tactics,
            roles=extracted.roles,
            request=extracted.request,
            pretext=extracted.pretext,
            persuasion_principles=extracted.persuasion_principles,
            timing=extracted.timing,
            impact=extracted.impact,
            information_website=info_website,
            coding_date=current_utc_zulu(),
            coder=request.coder,
            license=extracted.license,
            note_on_ambiguity=note,
            agreement_rate=DEFAULT_AGREEMENT_RATE,
        )

        if request.save_to_disk:
            if gates.is_excluded and exclusion_entry:
                saved_paths.extend(AtlasStorageService.save_exclusion_log(exclusion_entry))
            saved_paths.extend(
                AtlasStorageService.save_campaign(
                    campaign=campaign_record,
                    folder_slug=request.folder_slug,
                )
            )

        return CodeCampaignResponse(
            status="excluded" if gates.is_excluded else "coded",
            gates_evaluation=gates,
            campaign=campaign_record,
            exclusion_log_entry=exclusion_entry,
            source_metadata=metadata,
            saved_paths=saved_paths,
        )

    def code_report(self, request: CodeReportRequest) -> CodeReportResponse:
        """Code an Aggregate Report across the 4 sequential phases of CODING ORDER V1.0."""
        text, metadata = self._resolve_input_document(request.raw_text, request.url)
        user_prompt = build_report_coding_user_prompt(
            text=text,
            url=request.url,
            metadata=metadata,
        )

        extracted = self.llm_client.extract(
            response_model=ReportLLMExtraction,
            system_prompt=REPORT_CODING_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            override=request.llm_config,
            phase="coding",
        )

        report_id = request.report_id or AtlasStorageService.next_report_id()
        publisher = extracted.publisher or NOT_SPECIFIED_REPORT
        publisher_type = derive_publisher_type(publisher, fallback=extracted.publisher_type)
        info_website = (
            request.url
            or (metadata.url if metadata else None)
            or NOT_SPECIFIED_REPORT
        )

        report_record = ReportRecord(
            report_id=report_id,
            report_name=extracted.report_name,
            report_type=extracted.report_type,
            period_report=extracted.period_report,
            report_year=extracted.report_year,
            geographic_scope=extracted.geographic_scope,
            publisher=publisher,
            publisher_type=publisher_type,
            data_source=extracted.data_source,
            incident_counts=extracted.incident_counts,
            financial_loss=extracted.financial_loss,
            information_website=info_website,
            coding_date=current_utc_zulu(),
            coder=request.coder,
            license=extracted.license,
            note_on_ambiguity=extracted.note_on_ambiguity,
            agreement_rate=DEFAULT_AGREEMENT_RATE,
        )

        saved_paths: list[str] = []
        if request.save_to_disk:
            saved_paths = AtlasStorageService.save_report(
                report=report_record,
                folder_slug=request.folder_slug,
            )

        return CodeReportResponse(
            status="coded",
            report=report_record,
            source_metadata=metadata,
            saved_paths=saved_paths,
        )
