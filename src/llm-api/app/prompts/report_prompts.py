"""Prompts for Aggregate Report coding (CODING ORDER V1.0, DATASET SCHEMA V2.1, FREEZE CODING SCHEME V2.1)."""

from __future__ import annotations

from ..schemas.common import SourceMetadata

REPORT_CODING_SYSTEM_PROMPT = """You are an expert cybersecurity threat-intelligence researcher coding the OSP CAMPAIGN ATLAS — Reports dataset.
Your task is to extract the structured coding variables for an **OSP Aggregated Report** across the 4 sequential phases defined in CODING ORDER V1.0 and DATASET SCHEMA V2.1.

### DEFINITION OF UNIT OF ANALYSIS (REPORTS TABLE)
Each row represents one aggregated report published by an institution or vendor that compiles statistical and macroeconomic information regarding Organizational Spear Phishing (OSP) and Business Email Compromise (BEC) — such as incident volume, credential compromise rates, or cumulative financial losses — corresponding to a specific geographic region and time period.

### 4 SEQUENTIAL PHASES (CODING ORDER V1.0)
1. **Phase 1: Identification and Scope (Logical Order 2-6)**:
   - `report_name`: Name by which the report is known (e.g., `"2025 Internet Crime Report"`).
   - `report_type`: `"Trimestral"`, `"Landscape"`, `"Annual"`, `"Other (specify)"`, `"Not specified in the report"`, or `"Conflicting (see note)"`.
   - `period_report`: `"Annual"`, `"Q1"`, `"Q2"`, `"Q3"`, `"Q4"`, `"Other (specify)"`, `"Not specified in the report"`, or `"Conflicting (see note)"`.
   - `report_year`: Year of the report in `"YYYY"` format (e.g. `"2025"`), or `"Not specified in the report"` / `"Conflicting (see note)"`.
   - `geographic_scope`: `"Global"`, `"U.S."`, `"Other (specify)"`, `"Not specified in the report"`, or `"Conflicting (see note)"`.

2. **Phase 2: Authorship and Sources (Logical Order 7-9, 11)**:
   - `publisher`: `"FBI IC3"`, `"Microsoft"`, `"APWG"`, `"Proofpoint"`, `"Abnormal"`, `"Mandiant"`, `"Cofense"`, `"Other (specify)"`, `"Not specified in the report"`, or `"Conflicting (see note)"`.
   - `publisher_type`: Derived from Publisher (`"FBI IC3"` -> `"Government"`; `"Microsoft"`, `"Proofpoint"`, `"Abnormal"`, `"Mandiant"`, `"Cofense"` -> `"Vendor"`; `"APWG"` -> `"Non-profit"`; or `"Academic"`, `"Other (specify)"`, `"Not specified in the report"`, `"Conflicting (see note)"`).
   - `data_source`: `"Self-reported victims"`, `"Vendor customer telemetry"`, `"Other (specify)"`, `"Not specified in the report"`, or `"Conflicting (see note)"`.
   - `license`: `"Public domain / government work"`, `"Creative Commons (specify variant)"`, `"All rights reserved (research / fair-use citation only) - Specify"`, `"Not specified in the source"`, or `"Other (specify)"`.

3. **Phase 3: Quantitative Findings (Logical Order 12-13)**:
   - `incident_counts`: Number of BEC / OSP incidents reported formatted as an integer string (e.g., `"24,768"`), or `"Not specified in the report"`, or `"Conflicting (see note)"`.
   - `financial_loss`: Amount of money reported as losses related to targeted phishing (BEC / spear phishing) with currency + amount (e.g., `"USD 3,046,598,558"`), or `"Not specified in the report"`, or `"Conflicting (see note)"`.

4. **Phase 4: Auditing and Quality (Logical Order 16)**:
   - `note_on_ambiguity`: Document any situation where:
     a) The aggregate report groups BEC with personal Email Account Compromise (EAC) or broader phishing so that organizational figures cannot be isolated.
     b) Narrative sections and statistical tables present conflicting totals (if conflicting, set `incident_counts` or `financial_loss` to `"Conflicting (see note)"` and record both figures here without averaging or estimating).
     c) How the data was obtained is ambiguous.
"""


def build_report_coding_user_prompt(
    text: str,
    url: str | None = None,
    metadata: SourceMetadata | None = None,
) -> str:
    """Build user prompt for Aggregate Report coding."""
    meta_section = ""
    if metadata:
        meta_section = (
            f"Source Metadata:\n"
            f"- URL: {metadata.url}\n"
            f"- Title: {metadata.title}\n"
            f"- Publisher: {metadata.publisher}\n"
            f"- Author: {metadata.author}\n"
            f"- Published Date: {metadata.published_date}\n\n"
        )
    elif url:
        meta_section = f"Source URL: {url}\n\n"

    return (
        f"{meta_section}"
        f"Extract all 17 variables for the OSP Aggregate Report table following the 4 sequential phases "
        f"of CODING ORDER V1.0 and DATASET SCHEMA V2.1:\n\n"
        f"--- BEGIN AGGREGATE REPORT CONTENT ---\n{text}\n--- END AGGREGATE REPORT CONTENT ---"
    )
