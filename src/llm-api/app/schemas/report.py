"""Pydantic schemas for Aggregate Report coding matching CODING ORDER V1.0 and DATASET SCHEMA V2.1."""

from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from .common import (
    DEFAULT_AGREEMENT_RATE,
    NOT_SPECIFIED_REPORT,
    NOT_SPECIFIED_SOURCE,
    current_utc_zulu,
    derive_publisher_type,
)


class ReportLLMExtraction(BaseModel):
    """Structured LLM extraction model for Aggregate Reports following the 4 sequential phases of CODING ORDER V1.0."""

    # Phase 1: Identification and Scope (Logical Order 2-6)
    report_name: str = Field(..., description="Logical Order 2: Name by which the report is known.")
    report_type: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 3: Allowed values: 'Trimestral', 'Landscape', 'Annual', "
            "'Other (specify)', 'Not specified in the report', 'Conflicting (see note)'."
        ),
    )
    period_report: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 4: Period covered by the report: 'Annual', 'Q1', 'Q2', 'Q3', 'Q4', "
            "'Other (specify)', 'Not specified in the report', 'Conflicting (see note)'."
        ),
    )
    report_year: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description="Logical Order 5: Year of the report in YYYY format, or 'Not specified in the report' / 'Conflicting (see note)'.",
    )
    geographic_scope: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 6: Geographic area covered: 'Global', 'U.S.', 'Other (specify)', "
            "'Not specified in the report', 'Conflicting (see note)'."
        ),
    )

    # Phase 2: Authorship and Sources (Logical Order 7-9, 11)
    publisher: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 7: Organization publishing the report: 'FBI IC3', 'Microsoft', 'APWG', "
            "'Proofpoint', 'Abnormal', 'Mandiant', 'Cofense', 'Other (specify)', 'Not specified in the report', 'Conflicting (see note)'."
        ),
    )
    publisher_type: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 8: Institution type ('Government', 'Vendor', 'Academic', 'Non-profit', "
            "'Other (specify)', 'Not specified in the report', 'Conflicting (see note)')."
        ),
    )
    data_source: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 9: How the data was obtained: 'Self-reported victims', 'Vendor customer telemetry', "
            "'Other (specify)', 'Not specified in the report', 'Conflicting (see note)'."
        ),
    )
    license: str = Field(
        default=NOT_SPECIFIED_SOURCE,
        description=(
            "Logical Order 11: Usage license declared by publisher: 'Public domain / government work', "
            "'Creative Commons (specify variant)', 'All rights reserved (research / fair-use citation only) - Specify', "
            "'Not specified in the source', 'Other (specify)'."
        ),
    )

    # Phase 3: Quantitative Findings (Logical Order 12-13)
    incident_counts: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 12: Number of BEC/OSP incidents reported (formatted integer string e.g. '24,768'), "
            "or 'Not specified in the report' / 'Conflicting (see note)'."
        ),
    )
    financial_loss: str = Field(
        default=NOT_SPECIFIED_REPORT,
        description=(
            "Logical Order 13: Amount of money reported as losses related to targeted phishing (BEC / spear phishing) "
            "with currency + amount (e.g., 'USD 3,046,598,558'), or 'Not specified in the report' / 'Conflicting (see note)'."
        ),
    )

    # Phase 4: Auditing and Quality (Logical Order 16)
    note_on_ambiguity: str = Field(
        default="",
        description=(
            "Logical Order 16: Document any situation where the aggregate report does not clearly indicate whether a figure "
            "corresponds exclusively to BEC or broader OSP/EAC, does not specify how data was obtained, or has conflicting tables."
        ),
    )


class ReportRecord(BaseModel):
    """Canonical Report JSON schema matching `schemas/reports/report-schema.json`."""

    report_id: str = Field(..., description="Unique report identifier (e.g., REP-0001).")
    report_name: str
    report_type: str
    period_report: str
    report_year: str
    geographic_scope: str
    publisher: str
    publisher_type: str
    data_source: str
    incident_counts: str
    financial_loss: str
    information_website: str
    coding_date: str = Field(default_factory=current_utc_zulu)
    coder: str = Field(default="LLM assisted")
    license: str
    note_on_ambiguity: str = Field(default="")
    agreement_rate: str = Field(default=DEFAULT_AGREEMENT_RATE)

    @model_validator(mode="after")
    def enforce_dataset_rules(self) -> "ReportRecord":
        """Enforce deterministic Publisher -> Publisher Type and Decision Rule #11 for Agreement Rate."""
        self.publisher_type = derive_publisher_type(self.publisher, fallback=self.publisher_type)
        if self.coder.strip().lower() != "dual coded":
            self.agreement_rate = DEFAULT_AGREEMENT_RATE
        return self
