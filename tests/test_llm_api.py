"""Unit tests for the OSP Campaign Atlas LLM API (`src/llm-api/app`)."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path
from typing import TypeVar
from pydantic import BaseModel

# ``llm-api`` is a directory name, so it cannot be addressed as the
# ``src.llm_api`` dotted module used here originally.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "llm-api"))

from app.schemas.api import (  # type: ignore[reportMissingImports]
    CodeCampaignRequest,
    CodeReportRequest,
    DatasetAgreementRequest,
    EvaluateGatesRequest,
    ModelOverrideConfig,
    RowAgreementRequest,
    ValidateRecordRequest,
)
from app.schemas.campaign import (  # type: ignore[reportMissingImports]
    CampaignGatesEvaluation,
    CampaignLLMExtraction,
    CampaignRoles,
)
from app.schemas.report import ReportLLMExtraction  # type: ignore[reportMissingImports]
from app.services.agreement import (  # type: ignore[reportMissingImports]
    compute_dataset_agreement,
    compute_row_agreement,
    validate_atlas_record,
)
from app.services.coder import AtlasCodingService  # type: ignore[reportMissingImports]

T = TypeVar("T", bound=BaseModel)


class StubLLMClient:
    """Deterministic stub replacing LiteLLM network calls for unit testing."""

    def __init__(
        self,
        gates_result: CampaignGatesEvaluation | None = None,
        campaign_extraction: CampaignLLMExtraction | None = None,
        report_extraction: ReportLLMExtraction | None = None,
    ) -> None:
        self.gates_result = gates_result
        self.campaign_extraction = campaign_extraction
        self.report_extraction = report_extraction
        self.calls: list[type[BaseModel]] = []

    def extract(
        self,
        response_model: type[T],
        system_prompt: str,
        user_prompt: str,
        override: ModelOverrideConfig | None = None,
        phase: str = "default",
    ) -> T:
        self.calls.append(response_model)
        if response_model is CampaignGatesEvaluation and self.gates_result is not None:
            return self.gates_result  # type: ignore[return-value]
        if response_model is CampaignLLMExtraction and self.campaign_extraction is not None:
            return self.campaign_extraction  # type: ignore[return-value]
        if response_model is ReportLLMExtraction and self.report_extraction is not None:
            return self.report_extraction  # type: ignore[return-value]
        raise AssertionError(f"Unexpected response_model: {response_model}")


class LLMAPITestCase(unittest.TestCase):
    """Tests for 2-phase Campaign coding, Gate exclusions, Report coding, Agreement Rate & Cohen's kappa."""

    def test_gate_1_exclusion_stops_phase_2(self) -> None:
        gates = CampaignGatesEvaluation(
            campaign_name="Mass CAPTCHA Lumma Delivery",
            publisher="Microsoft Threat Intelligence",
            attack_classification="No target selection (OUT OF SCOPE)",
            case_source_type="Standalone campaign report",
            campaign_specificity="Single campaign",
            target="General internet users",
            targeting_evidence="Not specified in the report",
            has_isolable_sequence_details=True,
            is_excluded=True,
            rule_triggered="Rule #1",
            exclusion_reason="Opportunistic mass delivery with no organizational target selection.",
        )
        stub = StubLLMClient(gates_result=gates)
        service = AtlasCodingService(llm_client=stub)  # type: ignore[arg-type]

        response = service.code_campaign(
            CodeCampaignRequest(
                raw_text="Report describing mass drive-by ClickFix lures...",
                url="https://example.com/lumma",
                excluded_id="EXC-9999",
                save_to_disk=False,
            )
        )

        self.assertEqual(response.status, "excluded")
        self.assertIsNone(response.campaign)
        self.assertIsNotNone(response.exclusion_log_entry)
        self.assertEqual(response.exclusion_log_entry.rule_triggered, "Rule #1")
        # Ensure Phase 2 LLM extraction was NOT called (saved tokens)
        self.assertEqual(len(stub.calls), 1)
        self.assertIs(stub.calls[0], CampaignGatesEvaluation)

    def test_two_phase_campaign_coding_eligible(self) -> None:
        gates = CampaignGatesEvaluation(
            campaign_name="Storm-2755 Payroll Pirate",
            publisher="Microsoft Threat Intelligence",
            attack_classification="Hybrid Campaign - Targeting and impersonation necessary (other vector - specify)",
            hybrid_other_vector="SEO poisoning / malvertising, AiTM",
            case_source_type="Standalone campaign report",
            campaign_specificity="Single campaign",
            target="Canadian employees",
            targeting_evidence="Explicit targeting of Canadian employees and HR staff.",
            has_isolable_sequence_details=True,
        )
        extraction = CampaignLLMExtraction(
            campaign_name="Storm 2755 Payroll pirate attacks",
            publisher="Microsoft Threat Intelligence",
            publisher_type="Vendor",
            publication_date="2026-04-09",
            roles=CampaignRoles(
                role_attacker="Storm-2755",
                role_impersonated="Employee",
                role_victim="HR or finance staff members",
            ),
            channels="Search engine (SEO poisoning/malvertising) > Corporate email > HR SaaS platform (Workday)",
            channel_transition="Multiple transitions",
            tactics=[
                "Adversary-in-the-middle (AiTM)",
                "Compromised legitimate account (ATO)",
                "Mailbox rule manipulation",
            ],
            pretext="Setting up a new banking package before the upcoming pay date",
            request="Change direct deposit details to redirect a payroll check",
            persuasion_principles=["Urgency"],
            persuasion_principles_inferred=True,
            outcome="Successful (funds/data/credentials/access obtained)",
            impact="Direct financial loss due to diverted salary payments",
            timing="Payroll cycle",
            license="All rights reserved (research / fair-use citation only) - © Microsoft 2026",
            note_on_ambiguity="None",
        )
        stub = StubLLMClient(gates_result=gates, campaign_extraction=extraction)
        service = AtlasCodingService(llm_client=stub)  # type: ignore[arg-type]

        response = service.code_campaign(
            CodeCampaignRequest(
                campaign_id="CMP-9999",
                raw_text="Detailed Microsoft report on Storm-2755...",
                url="https://www.microsoft.com/en-us/security/blog/storm-2755",
                save_to_disk=False,
            )
        )

        self.assertEqual(response.status, "coded")
        self.assertEqual(len(stub.calls), 2)
        self.assertIsNotNone(response.campaign)
        assert response.campaign is not None
        self.assertEqual(response.campaign.campaign_id, "CMP-9999")
        self.assertEqual(
            response.campaign.attack_classification,
            "Hybrid Campaign - Targeting and impersonation necessary (SEO poisoning / malvertising, AiTM)",
        )
        self.assertEqual(response.campaign.publisher_type, "Vendor")
        self.assertEqual(response.campaign.agreement_rate, "N/A")
        self.assertIn("Inferred", response.campaign.note_on_ambiguity)

    def test_row_and_dataset_agreement_cohens_kappa(self) -> None:
        sample_a = {
            "campaign_id": "CMP-0001",
            "campaign_name": "Storm 2755",
            "publisher": "Microsoft Threat Intelligence",
            "publisher_type": "Vendor",
            "publication_date": "2026-04-09",
            "case_source_type": "Standalone campaign report",
            "campaign_specificity": "Single campaign",
            "attack_classification": "Pure BEC (Impersonation + Fraud)",
            "targeting_evidence": "Named organization",
            "outcome": "Successful (funds/data/credentials/access obtained)",
            "target": "Canadian employees",
            "channels": "Email",
            "channel_transition": "None (single channel throughout)",
            "tactics": ["Display - name spoofing", "Domain spoofing"],
            "roles": {
                "role_attacker": "Storm-2755",
                "role_impersonated": "CEO",
                "role_victim": "Finance",
            },
            "request": "Wire transfer",
            "pretext": "Urgent acquisition",
            "persuasion_principles": ["Authority", "Urgency"],
            "timing": "Invoice payment cycle",
            "impact": "Financial loss",
            "information_website": "https://example.com",
            "coding_date": "2026-10-20T08:28:00Z",
            "coder": "Dual coded",
            "license": "Not specified in the source",
            "note_on_ambiguity": "",
            "agreement_rate": "100%",
        }
        sample_b = dict(sample_a)

        row_res = compute_row_agreement(
            RowAgreementRequest(record_type="campaign", coder_a=sample_a, coder_b=sample_b)
        )
        self.assertEqual(row_res.agreement_rate, "100%")
        self.assertTrue(row_res.meets_protocol_threshold)

        ds_res = compute_dataset_agreement(
            DatasetAgreementRequest(
                coder_a_campaigns=[sample_a] * 5,
                coder_b_campaigns=[sample_b] * 5,
                min_label_frequency=5,
            )
        )
        self.assertEqual(ds_res.sample_size, 5)
        self.assertEqual(ds_res.mean_row_agreement_percentage, 100.0)
        self.assertEqual(ds_res.attack_classification.cohens_kappa, 1.0)

    def test_validate_record_auto_corrects_publisher_type_and_agreement_rate(self) -> None:
        payload = {
            "report_id": "REP-0011",
            "report_name": "2025 Internet Crime Report",
            "report_type": "Annual",
            "period_report": "Annual",
            "report_year": "2025",
            "geographic_scope": "Global",
            "publisher": "FBI IC3",
            "publisher_type": "Vendor",  # Incorrect: FBI IC3 must map to Government
            "data_source": "Self-reported victims",
            "incident_counts": "24,768",
            "financial_loss": "USD 3,046,598,558",
            "information_website": "https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf",
            "coding_date": "2026-10-25T11:21:39Z",
            "coder": "LLM assisted",
            "license": "Public domain / government work",
            "note_on_ambiguity": "",
            "agreement_rate": "95%",  # Must be reset to N/A when coder != Dual coded
        }
        res = validate_atlas_record(ValidateRecordRequest(record_type="report", payload=payload))
        self.assertTrue(res.valid)
        assert res.normalized_payload is not None
        self.assertEqual(res.normalized_payload["publisher_type"], "Government")
        self.assertEqual(res.normalized_payload["agreement_rate"], "N/A")


if __name__ == "__main__":
    unittest.main()
