"""Pydantic schemas for Campaign coding, Gate evaluation, and Exclusion Log."""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field, model_validator

from .common import (
    CONFLICTING_NOTE,
    DEFAULT_AGREEMENT_RATE,
    NOT_SPECIFIED_REPORT,
    OUT_OF_SCOPE_ATTACK_CLASSIFICATIONS,
    current_utc_zulu,
    derive_publisher_type,
)


class CampaignRoles(BaseModel):
    """Nested roles structure matching `schemas/campaigns/campaign-schema.json`."""

    role_attacker: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description="Identifies the attacker (e.g., threat actor name like Storm-2755, TA453, or 'Not specified in the report'). Never infer.",
    )
    role_impersonated: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description="Identifies the role impersonated by the attacker (e.g., 'CEO', 'Executive (unspecified)', 'Vendor/Supplier', or 'Not specified in the report'). Never infer.",
    )
    role_victim: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description="Identifies the victim role or group targeted within the organization (e.g., 'HR or finance staff members', or 'Not specified in the report'). Never infer.",
    )


class CampaignGatesEvaluation(BaseModel):
    """Phase 1 (Eligibility Filters: Gates 1-3) and Phase 2 (Target Identification) from CODING ORDER V1.0."""

    campaign_name: str = Field(
        ...,
        description="Name by which the candidate campaign or report is known.",
    )
    publisher: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description="Publisher of the report (e.g., 'Microsoft Threat Intelligence', 'Proofpoint', 'Abnormal', 'Mandiant', 'Cofense', 'APWG', 'FBI IC3', 'Other (specify)', 'Not specified in the report').",
    )
    # Logical Order 1 - GATE #1 (Evaluate First)
    attack_classification: Literal[
        "Pure BEC (Impersonation + Fraud)",
        "Pure Spear Phishing (Targeted lure + Impersonation)",
        "Hybrid Campaign - Targeting and impersonation necessary (other vector - specify)",
        "Impersonation unnecessary (OUT OF SCOPE)",
        "No target selection (OUT OF SCOPE)",
    ] = Field(
        ...,
        description=(
            "GATE #1 (Rule #1 - Evaluate First): "
            "'Pure BEC (Impersonation + Fraud)', 'Pure Spear Phishing (Targeted lure + Impersonation)', "
            "'Hybrid Campaign - Targeting and impersonation necessary (other vector - specify)', "
            "'Impersonation unnecessary (OUT OF SCOPE)', or 'No target selection (OUT OF SCOPE)'."
        ),
    )
    hybrid_other_vector: str | None = Field(
        default=None,
        description=(
            "Required ONLY when attack_classification is Hybrid Campaign. "
            "Specify the additional vector(s) needed before or alongside impersonation (e.g., 'SEO poisoning / malvertising, AiTM')."
        ),
    )
    # Logical Order 2 - GATE #2 (Evaluate Second)
    case_source_type: Literal[
        "Standalone campaign report",
        "Illustrative case within aggregate report",
        "Non-real life case (OUT OF SCOPE)",
    ] = Field(
        ...,
        description="GATE #2 (Rule #2 - Evaluate Second): Whether the campaign comes from a standalone report, an illustrative case within an aggregate report, or a non-real life case (demo/hypothetical).",
    )
    # Logical Order 3 - GATE #3 (Evaluate Third)
    campaign_specificity: Literal[
        "Single campaign",
        "Multi-Campaign aggregate / Generalized trend (OUT OF SCOPE)",
    ] = Field(
        ...,
        description=(
            "GATE #3 (Rule #3 - Evaluate Third): Whether the entry represents a single, distinguishable spear phishing incident "
            "with an isolable sequence of events (channel, role, pretext), or a generalized trend/multi-campaign aggregate."
        ),
    )
    # Logical Order 4 & 5 - Phase 2: Target Identification
    target: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description="Logical Order 4: The specific demographic, organization, industry, or region the attacker is targeting.",
    )
    targeting_evidence: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 5 (Test for targeting): Explicit evidence in the report that the organization, sector segment, or role "
            "was deliberately selected. If no explicit evidence is present, MUST be 'Not specified in the report'."
        ),
    )
    has_isolable_sequence_details: bool = Field(
        default=True,
        description=(
            "Decision Rule #8 check: Does the report provide sufficient explicit details to isolate a single campaign sequence "
            "(specifically channel, role, and pretext)?"
        ),
    )
    is_excluded: bool = Field(
        default=False,
        description="True if any of Gate #1, Gate #2, or Gate #3 triggers an OUT OF SCOPE exclusion.",
    )
    rule_triggered: Literal["Rule #1", "Rule #2", "Rule #3"] | None = Field(
        default=None,
        description="Which exclusion rule was triggered first (evaluated strictly in order: Rule #1 -> Rule #2 -> Rule #3). None if eligible.",
    )
    exclusion_reason: str | None = Field(
        default=None,
        description="Concrete sentence justifying the exclusion against the written definition in FREEZE CODING SCHEME V2.1. None if eligible.",
    )

    @model_validator(mode="after")
    def enforce_mandatory_gate_order(self) -> "CampaignGatesEvaluation":
        """Enforce the strict mandatory evaluation order (Rule #1 -> Rule #2 -> Rule #3) and Test for Targeting."""
        # Rule #1 check: Attack Classification or absence of explicit targeting evidence
        if (
            self.attack_classification in OUT_OF_SCOPE_ATTACK_CLASSIFICATIONS
            or self.targeting_evidence.strip().lower() == NOT_SPECIFIED_REPORT.lower()
        ):
            self.is_excluded = True
            self.rule_triggered = "Rule #1"
            if not self.exclusion_reason:
                self.exclusion_reason = (
                    "The campaign fails Rule #1 (Attack Classification / Test for targeting): "
                    "it lacks explicit evidence of deliberate target selection against an organization/role "
                    "or impersonation is not part of the attack path."
                )
            return self

        # Rule #2 check: Case Source Type
        if self.case_source_type == "Non-real life case (OUT OF SCOPE)":
            self.is_excluded = True
            self.rule_triggered = "Rule #2"
            if not self.exclusion_reason:
                self.exclusion_reason = (
                    "The campaign fails Rule #2 (Case Source Type): "
                    "it is not based on a real-life incident (e.g., hypothetical, training, or demo example)."
                )
            return self

        # Rule #3 check: Campaign Specificity or Decision Rule #8 (insufficient detail for sequence)
        if (
            self.campaign_specificity == "Multi-Campaign aggregate / Generalized trend (OUT OF SCOPE)"
            or not self.has_isolable_sequence_details
        ):
            self.is_excluded = True
            self.rule_triggered = "Rule #3"
            if not self.exclusion_reason:
                self.exclusion_reason = (
                    "The campaign fails Rule #3 (Campaign Specificity / Decision Rule #8): "
                    "the report presents generalized trends or lacks sufficient detail (channel, role, pretext) "
                    "to isolate a single, distinguishable organizational spear phishing sequence."
                )
            return self

        self.is_excluded = False
        self.rule_triggered = None
        self.exclusion_reason = None
        return self

    def formatted_attack_classification(self) -> str:
        """Format Hybrid Campaign classification with its specified vector as required by FREEZE CODING SCHEME V2.1."""
        if self.attack_classification.startswith("Hybrid Campaign"):
            vector = (self.hybrid_other_vector or "other vector - specify").strip()
            return f"Hybrid Campaign - Targeting and impersonation necessary ({vector})"
        return self.attack_classification


class CampaignLLMExtraction(BaseModel):
    """Structured extraction model for Phases 3 to 8 of CODING ORDER V1.0 (used in Stage 2 after Gates pass)."""

    # Phase 3: Identity and Sources (Logical Order 7-10)
    campaign_name: str = Field(..., description="Logical Order 7: Name by which the campaign is known.")
    publisher: str = Field(
        ...,
        description=(
            "Logical Order 8: Organization publishing the report. Allowed: 'Microsoft Threat Intelligence', 'Proofpoint', "
            "'Abnormal', 'Mandiant', 'Cofense', 'APWG', 'FBI IC3', 'Other (specify)', 'Not specified in the report', 'Conflicting (see note)'."
        ),
    )
    publisher_type: str = Field(
        ...,
        description=(
            "Logical Order 9: Institution type ('Government', 'Vendor', 'Academic', 'Non-profit', "
            "'Other (specify)', 'Not specified in the report', 'Conflicting (see note)')."
        ),
    )
    publication_date: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description="Logical Order 10: Publication date in YYYY-MM-DD format, or 'Not specified in the report' / 'Conflicting (see note)'.",
    )

    # Phase 4: Involved Actors (Logical Order 12-14) - Zero-inference rule!
    roles: CampaignRoles = Field(
        ...,
        description=(
            "Logical Order 12-14: Attacker, Impersonated Role, and Victim. "
            "ZERO-INFERENCE RULE: Never infer roles not explicitly stated. If generic executive, use 'Executive (unspecified)'. "
            "If absent, use 'Not specified in the report'."
        ),
    )

    # Phase 5: Vectors and Execution (Logical Order 15-17)
    channels: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 15: Communication medium or technical vector path (e.g., 'Corporate email > HR SaaS platform (Workday)'). "
            "ZERO-INFERENCE RULE: Never infer channels; if absent, use 'Not specified in the report'."
        ),
    )
    channel_transition: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 16: Allowed values: 'None (single channel throughout)', 'Email > Phone call', 'Email > Messaging app', "
            "'Different email thread/domain', 'Multiple transitions', 'Other (specify)', 'Not specified in the report', 'Conflicting (see note)'."
        ),
    )
    tactics: list[str] = Field(
        default_factory=lambda: [NOT_SPECIFIED_REPORT],
        description=(
            "Logical Order 17: Multi-value list of tactics from the Tactics Taxonomy. Record ALL applicable values. "
            "Rule: if session-cookie capture or MFA bypass is described alongside a fake login page, include BOTH "
            "'Fake login / credential-collection page' and 'Adversary-in-the-middle (AiTM)'."
        ),
    )

    # Phase 6: Social Engineering (Logical Order 18-20)
    pretext: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 18: The fabricated story or social-engineering lure used by the attacker. "
            "ZERO-INFERENCE RULE: Never infer pretext; if absent, use 'Not specified in the report'."
        ),
    )
    request: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description="Logical Order 19: The final action the attacker wants the victim to perform (transfer funds, click link, disclose credentials, etc.).",
    )
    persuasion_principles: list[str] = Field(
        default_factory=lambda: [NOT_SPECIFIED_REPORT],
        description=(
            "Logical Order 20: Multi-value list from taxonomy ('Reciprocity', 'Consistency', 'Social Proof', 'Authority', "
            "'Liking', 'Scarcity', 'Commitment', 'Urgency', 'Other (specify)', 'Not specified in the report'). "
            "EXCEPTION RULE: May be inferred latently strictly and exclusively from the explicit text of the pretext or request."
        ),
    )
    persuasion_principles_inferred: bool = Field(
        default=False,
        description="True if persuasion_principles were inferred latently from the pretext/request rather than named explicitly in the report.",
    )

    # Phase 7: Outcomes (Logical Order 21-23)
    outcome: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 21: Allowed values: 'Successful (funds/data/credentials/access obtained)', "
            "'Thwarted / Prevented', 'Partial', 'Not specified in the report', 'Conflicting (see note)'."
        ),
    )
    impact: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description="Logical Order 22: Final consequence or damage caused by the attack, or 'Not specified in the report'.",
    )
    timing: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 23: Allowed values: 'Real estate closing', 'Invoice payment cycle', 'Holiday', 'Payroll cycle', "
            "'Other (specify)', 'Not specific', 'Not specified in the report', 'Conflicting (see note)'. "
            "ZERO-INFERENCE RULE: Never infer timing."
        ),
    )

    # Phase 8: Auditing and Quality (Logical Order 24, 27)
    license: str = Field(
        default="Not specified in the source",
        description=(
            "Logical Order 24: Usage license declared by publisher: 'Public domain / government work', "
            "'Creative Commons (specify variant)', 'All rights reserved (research / fair-use citation only) - Specify', "
            "'Not specified in the source', or 'Other (specify)'."
        ),
    )
    note_on_ambiguity: str = Field(
        default="None",
        description=(
            "Logical Order 27: Document any conflicting data points, inferred persuasion principles, "
            "additional consolidated reports, or unresolvable ambiguities."
        ),
    )


class CampaignRecord(BaseModel):
    """Canonical Campaign JSON schema matching `schemas/campaigns/campaign-schema.json`."""

    campaign_id: str = Field(..., description="Unique campaign identifier (e.g., CMP-0001).")
    campaign_name: str
    publisher: str
    publisher_type: str
    publication_date: str
    case_source_type: str
    campaign_specificity: str
    attack_classification: str
    targeting_evidence: str
    outcome: str
    target: str
    channels: str
    channel_transition: str
    tactics: list[str]
    roles: CampaignRoles
    request: str
    pretext: str
    persuasion_principles: list[str]
    timing: str
    impact: str
    information_website: str
    coding_date: str = Field(default_factory=current_utc_zulu)
    coder: str = Field(default="LLM assisted")
    license: str
    note_on_ambiguity: str = Field(default="")
    agreement_rate: str = Field(default=DEFAULT_AGREEMENT_RATE)

    @model_validator(mode="after")
    def enforce_dataset_rules(self) -> "CampaignRecord":
        """Enforce deterministic Publisher -> Publisher Type and Decision Rule #11 for Agreement Rate."""
        self.publisher_type = derive_publisher_type(self.publisher, fallback=self.publisher_type)
        if self.coder.strip().lower() != "dual coded":
            self.agreement_rate = DEFAULT_AGREEMENT_RATE
        if not self.tactics:
            self.tactics = [NOT_SPECIFIED_REPORT]
        if not self.persuasion_principles:
            self.persuasion_principles = [NOT_SPECIFIED_REPORT]
        return self


class ExclusionLogRecord(BaseModel):
    """Canonical Exclusion Log entry matching `schemas/campaigns/exclusion-log-schema.json`."""

    excluded_id: str = Field(..., description="Unique excluded campaign identifier (e.g., EXC-0001).")
    campaign_name: str
    publisher: str
    information_website: str
    rule_triggered: str = Field(..., description="Rule #1, Rule #2, or Rule #3.")
    exclusion_reason: str = Field(..., description="Concrete sentence justifying the exclusion against the written definition.")
    exclusion_date: str = Field(default_factory=current_utc_zulu)
    evaluator: str = Field(default="LLM-API")
