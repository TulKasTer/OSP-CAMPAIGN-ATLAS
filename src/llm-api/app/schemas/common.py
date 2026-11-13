"""Common constants, taxonomies, and metadata schemas from FREEZE CODING SCHEME V2.1 and DATASET SCHEMA V2.1."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field

# Transversal escape values
NOT_SPECIFIED_REPORT = "Not specified in the report"
NOT_SPECIFIED_SOURCE = "Not specified in the source"
CONFLICTING_NOTE = "Conflicting (see note)"
OTHER_SPECIFY_PREFIX = "Other (specify)"
DEFAULT_AGREEMENT_RATE = "N/A"

# Allowed Publishers (Campaigns & Reports)
CAMPAIGN_PUBLISHERS = (
    "Microsoft Threat Intelligence",
    "Proofpoint",
    "Abnormal",
    "Mandiant",
    "Cofense",
    "APWG",
    "FBI IC3",
    "Other (specify)",
    NOT_SPECIFIED_REPORT,
    CONFLICTING_NOTE,
)

REPORT_PUBLISHERS = (
    "FBI IC3",
    "Microsoft",
    "Microsoft Threat Intelligence",
    "APWG",
    "Proofpoint",
    "Abnormal",
    "Mandiant",
    "Cofense",
    "Other (specify)",
    NOT_SPECIFIED_REPORT,
    CONFLICTING_NOTE,
)

PUBLISHER_TYPES = (
    "Government",
    "Vendor",
    "Academic",
    "Non-profit",
    "Other (specify)",
    NOT_SPECIFIED_REPORT,
    CONFLICTING_NOTE,
)

# Deterministic Publisher -> Publisher Type relation (FREEZE CODING SCHEME V2.1)
PUBLISHER_TO_TYPE_MAP: dict[str, str] = {
    "fbi ic3": "Government",
    "microsoft threat intelligence": "Vendor",
    "microsoft": "Vendor",
    "microsoft security blog": "Vendor",
    "proofpoint": "Vendor",
    "abnormal": "Vendor",
    "abnormal security": "Vendor",
    "mandiant": "Vendor",
    "cofense": "Vendor",
    "apwg": "Non-profit",
}

# Gate #1: Attack Classification
ATTACK_CLASSIFICATION_VALUES = (
    "Pure BEC (Impersonation + Fraud)",
    "Pure Spear Phishing (Targeted lure + Impersonation)",
    "Hybrid Campaign - Targeting and impersonation necessary (other vector - specify)",
    "Impersonation unnecessary (OUT OF SCOPE)",
    "No target selection (OUT OF SCOPE)",
)

OUT_OF_SCOPE_ATTACK_CLASSIFICATIONS = {
    "Impersonation unnecessary (OUT OF SCOPE)",
    "No target selection (OUT OF SCOPE)",
}

# Gate #2: Case Source Type
CASE_SOURCE_TYPE_VALUES = (
    "Standalone campaign report",
    "Illustrative case within aggregate report",
    "Non-real life case (OUT OF SCOPE)",
)

# Gate #3: Campaign Specificity
CAMPAIGN_SPECIFICITY_VALUES = (
    "Single campaign",
    "Multi-Campaign aggregate / Generalized trend (OUT OF SCOPE)",
)

# Channel Transition allowed values
CHANNEL_TRANSITION_VALUES = (
    "None (single channel throughout)",
    "Email > Phone call",
    "Email > Messaging app",
    "Different email thread/domain",
    "Multiple transitions",
    "Other (specify)",
    NOT_SPECIFIED_REPORT,
    CONFLICTING_NOTE,
)

# Tactics Taxonomy (DATASET SCHEMA V2.1)
TACTICS_TAXONOMY = (
    "Display - name spoofing",
    "Domain spoofing",
    "Typosquatting / lookalike domain",
    "Homoglyph domain spoofing",
    "Fake reply-chain / thread hijacking",
    "Reply-To header manipulation",
    "Message encoding / obfuscation",
    "Compromised legitimate account (ATO)",
    "Mailbox rule manipulation",
    "Adversary-in-the-middle (AiTM)",
    "Compromised third-party vendor account",
    "Malicious attachment",
    "Malicious link / redirect",
    "Fake login / credential-collection page",
    "Other (specify)",
    NOT_SPECIFIED_REPORT,
    CONFLICTING_NOTE,
)

# Persuasion Principles Taxonomy (Van Der Heijden & Allodi, 2019; Bullée et al., 2018; Papathanasiou et al., 2023)
PERSUASION_PRINCIPLES_TAXONOMY = (
    "Reciprocity",
    "Consistency",
    "Social Proof",
    "Authority",
    "Liking",
    "Scarcity",
    "Commitment",
    "Urgency",
    "Other (specify)",
    NOT_SPECIFIED_REPORT,
)

# Outcome values
OUTCOME_VALUES = (
    "Successful (funds/data/credentials/access obtained)",
    "Thwarted / Prevented",
    "Partial",
    NOT_SPECIFIED_REPORT,
    CONFLICTING_NOTE,
)

# Timing values
TIMING_VALUES = (
    "Real estate closing",
    "Invoice payment cycle",
    "Holiday",
    "Payroll cycle",
    "Other (specify)",
    "Not specific",
    NOT_SPECIFIED_REPORT,
    CONFLICTING_NOTE,
)

# Coder provenance values
CODER_VALUES = (
    "Human coded",
    "LLM assisted",
    "Human verified",
    "Dual coded",
)

# License values
LICENSE_VALUES = (
    "Public domain / government work",
    "Creative Commons (specify variant)",
    "All rights reserved (research / fair-use citation only) - Specify",
    NOT_SPECIFIED_SOURCE,
    "Other (specify)",
)

# Report specific closed values
REPORT_TYPE_VALUES = (
    "Trimestral",
    "Landscape",
    "Annual",
    "Other (specify)",
    NOT_SPECIFIED_REPORT,
    CONFLICTING_NOTE,
)

PERIOD_REPORT_VALUES = (
    "Annual",
    "Q1",
    "Q2",
    "Q3",
    "Q4",
    "Other (specify)",
    NOT_SPECIFIED_REPORT,
    CONFLICTING_NOTE,
)

GEOGRAPHIC_SCOPE_VALUES = (
    "Global",
    "U.S.",
    "Other (specify)",
    NOT_SPECIFIED_REPORT,
    CONFLICTING_NOTE,
)

DATA_SOURCE_VALUES = (
    "Self-reported victims",
    "Vendor customer telemetry",
    "Other (specify)",
    NOT_SPECIFIED_REPORT,
    CONFLICTING_NOTE,
)

ExclusionRuleLiteral = Literal["Rule #1", "Rule #2", "Rule #3"]


def derive_publisher_type(publisher: str, fallback: str | None = None) -> str:
    """Derive publisher_type deterministically from publisher per FREEZE CODING SCHEME V2.1."""
    normalized = (publisher or "").strip().lower().rstrip(".")
    if normalized in PUBLISHER_TO_TYPE_MAP:
        return PUBLISHER_TO_TYPE_MAP[normalized]
    if normalized == NOT_SPECIFIED_REPORT.lower():
        return NOT_SPECIFIED_REPORT
    if normalized == CONFLICTING_NOTE.lower():
        return CONFLICTING_NOTE
    if fallback and fallback.strip():
        return fallback.strip()
    return "Other (specify)"


def current_utc_zulu() -> str:
    """Return current UTC timestamp formatted as ISO 8601 Zulu (YYYY-MM-DDThh:mm:ssZ)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class SourceMetadata(BaseModel):
    """Schema matching `schemas/metadata-schema.json`."""

    url: str = Field(..., description="Source URL of the threat intelligence report.")
    title: str = Field(default="Not specified", description="Title of the document/webpage.")
    publisher: str = Field(default="Not specified", description="Publisher or site name.")
    author: str = Field(default="Not specified", description="Author(s) of the report.")
    published_date: str = Field(default="Not specified", description="Publication date extracted from metadata.")
    retrieved_at_utc: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="UTC timestamp when the resource was retrieved.",
    )
    sha256_hash: str = Field(..., description="SHA-256 hex digest of the raw document bytes.")
