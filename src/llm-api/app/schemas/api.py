"""Request and response schemas for the FastAPI endpoints."""

from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field, model_validator

from .campaign import CampaignGatesEvaluation, CampaignRecord, ExclusionLogRecord
from .common import SourceMetadata
from .report import ReportRecord


class ModelOverrideConfig(BaseModel):
    """Optional per-request LLM model, sampling, and RAM/VRAM configuration override."""

    model: str | None = Field(
        default=None,
        description="LiteLLM model string (e.g. 'ollama/qwen3.5:9b', 'openai/gpt-4o', 'gemini/gemini-2.5-pro'). Uses LLM_MODEL env var if omitted.",
    )
    api_key: str | None = Field(
        default=None,
        description="Optional API key override for the LLM provider.",
    )
    api_base: str | None = Field(
        default=None,
        description="Optional base URL override (e.g., for local Ollama or vLLM).",
    )
    temperature: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0,
        description="Sampling temperature override (defaults to LLM_TEMPERATURE in .env).",
    )
    top_p: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Nucleus sampling top_p override.",
    )
    top_k: int | None = Field(
        default=None,
        ge=1,
        description="Top-K sampling override (for local/Ollama models).",
    )
    max_tokens: int | None = Field(
        default=None,
        ge=64,
        description="Max output tokens override (max_tokens / num_predict).",
    )
    seed: int | None = Field(
        default=None,
        description="Random seed for reproducible generation.",
    )
    num_ctx: int | None = Field(
        default=None,
        ge=512,
        description="Context window size in tokens (Ollama num_ctx — directly controls KV-cache VRAM/RAM).",
    )
    num_gpu: int | None = Field(
        default=None,
        ge=-1,
        description="Number of model layers offloaded to GPU VRAM (-1 = all, 0 = CPU/RAM only, >0 = partial offload).",
    )
    num_thread: int | None = Field(
        default=None,
        ge=0,
        description="CPU thread count for layers running in system RAM (0 = auto).",
    )
    num_batch: int | None = Field(
        default=None,
        ge=16,
        description="Prompt processing batch size (lower reduces peak VRAM).",
    )
    keep_alive: str | None = Field(
        default=None,
        description="How long Ollama keeps the model loaded in VRAM after the request (e.g., '10m', '0', '-1').",
    )


class DocumentInputMixin(BaseModel):
    """Shared input mixin allowing raw text, a URL to fetch, or both."""

    raw_text: str | None = Field(
        default=None,
        description="Raw text or markdown content of the threat intelligence report.",
    )
    url: str | None = Field(
        default=None,
        description="URL of the threat intelligence report. If raw_text is omitted, the API fetches and extracts text from this URL.",
    )

    @model_validator(mode="after")
    def check_text_or_url(self) -> "DocumentInputMixin":
        if not (self.raw_text and self.raw_text.strip()) and not (self.url and self.url.strip()):
            raise ValueError("Must provide either 'raw_text' or 'url' (or both).")
        return self


class EvaluateGatesRequest(DocumentInputMixin):
    """Request payload for Stage 1 Campaign Eligibility Evaluation (Gates #1-#3)."""

    excluded_id: str | None = Field(
        default=None,
        description="Optional excluded_id (e.g., 'EXC-0055') if the campaign is excluded. Auto-generated if omitted.",
    )
    evaluator: str = Field(
        default="LLM-API",
        description="Evaluator identifier recorded in the Exclusion Log if excluded.",
    )
    save_to_disk: bool = Field(
        default=False,
        description="If True and the campaign is excluded, appends the ExclusionLogRecord to data/interim/llm-coded/campaigns/exclusion-log.json and logs/exclusion-log.log.",
    )
    llm_config: ModelOverrideConfig | None = None


class EvaluateGatesResponse(BaseModel):
    """Response payload for Stage 1 Campaign Eligibility Evaluation."""

    status: Literal["eligible", "excluded"]
    gates_evaluation: CampaignGatesEvaluation
    exclusion_log_entry: ExclusionLogRecord | None = None
    source_metadata: SourceMetadata | None = None
    saved_paths: list[str] = Field(default_factory=list)


class CodeCampaignRequest(DocumentInputMixin):
    """Request payload for 2-phase Campaign Coding (Gates #1-#3 -> 28 variables)."""

    campaign_id: str | None = Field(
        default=None,
        description="Campaign identifier (e.g., 'CMP-0059'). Auto-generated if omitted.",
    )
    excluded_id: str | None = Field(
        default=None,
        description="Exclusion log identifier (e.g., 'EXC-0055') used if the campaign fails Gates #1-#3. Auto-generated if omitted.",
    )
    folder_slug: str | None = Field(
        default=None,
        description="Optional folder slug when saving to data/interim/llm-coded/campaigns/<slug>/.",
    )
    coder: str = Field(
        default="LLM assisted",
        description="Coder provenance value ('LLM assisted', 'Human coded', 'Human verified', 'Dual coded').",
    )
    evaluator: str = Field(
        default="LLM-API",
        description="Evaluator identifier for Exclusion Log if excluded.",
    )
    force_full_coding: bool = Field(
        default=False,
        description="If True, executes Phase 2 full variable extraction even if Stage 1 Gates mark the campaign as excluded.",
    )
    save_to_disk: bool = Field(
        default=False,
        description="If True, persists the coded campaign or exclusion log entry into data/interim/llm-coded/.",
    )
    llm_config: ModelOverrideConfig | None = None


class CodeCampaignResponse(BaseModel):
    """Response payload for 2-phase Campaign Coding."""

    status: Literal["coded", "excluded"]
    gates_evaluation: CampaignGatesEvaluation
    campaign: CampaignRecord | None = None
    exclusion_log_entry: ExclusionLogRecord | None = None
    source_metadata: SourceMetadata | None = None
    saved_paths: list[str] = Field(default_factory=list)


class CodeReportRequest(DocumentInputMixin):
    """Request payload for Aggregate Report Coding (17 variables across 4 phases)."""

    report_id: str | None = Field(
        default=None,
        description="Report identifier (e.g., 'REP-0012'). Auto-generated if omitted.",
    )
    folder_slug: str | None = Field(
        default=None,
        description="Optional folder slug when saving to data/interim/llm-coded/reports/<slug>/.",
    )
    coder: str = Field(
        default="LLM assisted",
        description="Coder provenance value ('LLM assisted', 'Human coded', 'Human verified', 'Dual coded').",
    )
    save_to_disk: bool = Field(
        default=False,
        description="If True, persists the coded report into data/interim/llm-coded/reports/.",
    )
    llm_config: ModelOverrideConfig | None = None


class CodeReportResponse(BaseModel):
    """Response payload for Aggregate Report Coding."""

    status: Literal["coded"] = "coded"
    report: ReportRecord
    source_metadata: SourceMetadata | None = None
    saved_paths: list[str] = Field(default_factory=list)


class SourceMetadataRequest(BaseModel):
    """Request to fetch URL metadata and SHA-256 hash."""

    url: str = Field(..., description="HTTP(S) URL of the report to fetch.")
    include_extracted_text: bool = Field(
        default=False,
        description="If True, includes the cleaned plain text extracted from the HTML.",
    )
    save_to_disk: bool = Field(
        default=False,
        description="If True, saves metadata JSON and weblink TXT to data/raw/.",
    )
    target_type: Literal["campaigns", "reports"] = Field(
        default="campaigns",
        description="Whether to store under data/raw/campaigns or data/raw/reports when save_to_disk=True.",
    )
    folder_slug: str | None = Field(
        default=None,
        description="Subfolder name under data/raw/<target_type>/<folder_slug>/.",
    )


class SourceMetadataResponse(BaseModel):
    """Response containing extracted SourceMetadata and optional text."""

    metadata: SourceMetadata
    extracted_text: str | None = None
    saved_paths: list[str] = Field(default_factory=list)


class FieldComparisonResult(BaseModel):
    """Per-variable comparison details between Coder A and Coder B."""

    variable: str
    coder_a_value: Any
    coder_b_value: Any
    matched: bool
    similarity_score: float = Field(..., ge=0.0, le=1.0)


class RowAgreementRequest(BaseModel):
    """Request to compute row-level Agreement Rate between two independent codings."""

    record_type: Literal["campaign", "report"] = "campaign"
    coder_a: dict[str, Any] = Field(..., description="First independent coding JSON object.")
    coder_b: dict[str, Any] = Field(..., description="Second independent coding JSON object.")
    compare_only_closed_variables: bool = Field(
        default=False,
        description="If True, compares only closed/categorical and multi-label taxonomy variables. If False, compares all analytical variables.",
    )


class RowAgreementResponse(BaseModel):
    """Response with row-level percentage agreement and per-variable breakdown."""

    record_type: Literal["campaign", "report"]
    agreement_rate: str = Field(..., description="Formatted percentage string (e.g. '85%') for the 'agreement_rate' field.")
    agreement_percentage: float = Field(..., description="Numeric percentage (0.0 to 100.0).")
    matched_variables: int
    total_variables_compared: int
    meets_protocol_threshold: bool = Field(
        ...,
        description="True if row agreement >= 80% as specified in Registered Protocol V1.",
    )
    comparisons: list[FieldComparisonResult]


class DatasetAgreementRequest(BaseModel):
    """Request to compute Cohen's kappa (κ) and % agreement across a dual-coded sample of campaigns."""

    coder_a_campaigns: list[dict[str, Any]] = Field(
        ...,
        min_length=1,
        description="List of campaign JSON records from Coder A.",
    )
    coder_b_campaigns: list[dict[str, Any]] = Field(
        ...,
        min_length=1,
        description="List of campaign JSON records from Coder B (matched by campaign_id or index).",
    )
    min_label_frequency: int = Field(
        default=5,
        ge=1,
        description="Per Registered Protocol V1: labels appearing fewer than 5 times are reported with % agreement only.",
    )


class LabelKappaMetric(BaseModel):
    """Cohen's kappa and % agreement for a single variable or binary multi-label taxonomy item."""

    name: str
    occurrences_coder_a: int
    occurrences_coder_b: int
    percent_agreement: float
    cohens_kappa: float | None = Field(
        default=None,
        description="Cohen's kappa (κ). None if label appears fewer than min_label_frequency times.",
    )
    meets_criterion: bool = Field(
        ...,
        description="True if κ >= 0.60 (or percent_agreement >= 80.0 when κ is omitted due to low frequency).",
    )
    note: str | None = None


class DatasetAgreementResponse(BaseModel):
    """Dataset-level inter-rater agreement report matching Registered Protocol V1 (Agreement Measures table)."""

    sample_size: int
    mean_row_agreement_percentage: float
    attack_classification: LabelKappaMetric
    targeting_evidence_presence: LabelKappaMetric
    hybrid_other_vector_agreement_percentage: float | None = None
    persuasion_principles_per_label: list[LabelKappaMetric]
    tactics_per_label: list[LabelKappaMetric]
    row_results: list[RowAgreementResponse]


class ValidateRecordRequest(BaseModel):
    """Request to validate a Campaign, Report, or Exclusion Log JSON object against FREEZE CODING SCHEME V2.1 rules."""

    record_type: Literal["campaign", "report", "exclusion_log"] = "campaign"
    payload: dict[str, Any]


class ValidateRecordResponse(BaseModel):
    """Validation result with normalized record, errors, and warnings."""

    valid: bool
    record_type: Literal["campaign", "report", "exclusion_log"]
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    normalized_payload: dict[str, Any] | None = None
