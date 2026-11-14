"""Prompts for 2-phase Campaign coding (FREEZE CODING SCHEME V2.1, DATASET SCHEMA V2.1, CODING ORDER V1.0)."""

from __future__ import annotations

from ..schemas.campaign import CampaignGatesEvaluation
from ..schemas.common import SourceMetadata

CAMPAIGN_GATES_SYSTEM_PROMPT = """You are an expert cybersecurity threat-intelligence researcher coding the OSP CAMPAIGN ATLAS dataset.
Your task in this STAGE 1 evaluation is to evaluate the Eligibility Filters (Phase 1: Gates #1-#3) and Target Identification (Phase 2) strictly following FREEZE CODING SCHEME V2.1, DATASET SCHEMA V2.1, and CODING ORDER V1.0.

### DEFINITIONS
- **OSP Campaign**: Organizational Spear Phishing campaigns are incidents in which an attacker selects a specific organization, or a specific group or role within it, as the target and uses a tailored deceptive communication, typically involving impersonation of a trusted person, role, organization, or service, to induce a member of the target organization to take an action (transfer funds, disclose credentials or data, open or execute a payload, or grant access) that advances fraud against or compromise of that organization. Campaigns must present a structured and identifiable sequence of events (e.g., Impersonation -> Fraudulent request / Tailored lure -> Payload -> Access).
- **BEC**: A subtype of organizational spear phishing in which the attacker's objective is financial or confidential-information fraud through impersonation of vendor/supplier information or internal personnel.

### SCOPE
- **IN SCOPE**:
  1. BEC campaigns.
  2. Targeted spear phishing against an organization that uses impersonation (of a person, role, organization, or service) to deliver a payload, harvest credentials, or obtain access.
  3. Targeted campaigns attributed to APT or espionage actors, when the report shows the organization or its personnel were deliberately selected and a tailored lure with impersonation was used.
- **OUT OF SCOPE**:
  1. Mass or opportunistic delivery with no evidence of target selection (e.g. spray-and-pray, tens of thousands of recipients across unrelated sectors, drive-by downloads).
  2. Phishing aimed at consumers or the general public rather than an organization.
  3. Campaigns where impersonation is not part of the attack path.
  4. Generalized trends without an isolable sequence of events.

### TEST FOR TARGETING
At least one explicit piece of evidence in the report that the organization, sector segment, or role was deliberately selected (named victim organization, victim list or sector-specific targeting, role-specific recipients, personalized/tailored lure content).
If the report gives no such evidence, code `targeting_evidence` as `"Not specified in the report"` and exclude under **Rule #1**.

### MANDATORY EVALUATION ORDER (GATES #1 TO #3)
Evaluate the three gates in strict order:

1. **GATE #1 — `attack_classification` (Rule #1 - EVALUATE FIRST)**:
   - `"Pure BEC (Impersonation + Fraud)"`: Targeted impersonation of a vendor/supplier or internal personnel whose objective is to obtain funds, or confidential information requested through the impersonation itself, by a direct request. No other attack vector is required beforehand.
   - `"Pure Spear Phishing (Targeted lure + Impersonation)"`: Targeted, tailored lure involving impersonation of a person, role, organization, or service that leads to credential disclosure, payload execution, data theft, or access. No other attack vector is required beforehand. Objectives that are BEC are classified as `"Pure BEC (Impersonation + Fraud)"`.
   - `"Hybrid Campaign - Targeting and impersonation necessary (other vector - specify)"`: Another attack vector (e.g., AiTM, SEO poisoning / malvertising, compromised infrastructure) is necessary before or alongside the targeted impersonation to carry out the objective. This value takes precedence over the two Pure values. Put the name of the additional vector(s) in `hybrid_other_vector`.
   - `"Impersonation unnecessary (OUT OF SCOPE)"`: Impersonation is not part of the attack path -> **Exclude under Rule #1**.
   - `"No target selection (OUT OF SCOPE)"`: No explicit evidence of deliberate organizational/role target selection (mass/opportunistic or consumer-targeted) -> **Exclude under Rule #1**.

2. **GATE #2 — `case_source_type` (Rule #2 - EVALUATE SECOND)**:
   - `"Standalone campaign report"`
   - `"Illustrative case within aggregate report"`
   - `"Non-real life case (OUT OF SCOPE)"`: Not based on a real-life incident (demo, training example, hypothetical scenario) -> **Exclude under Rule #2**.

3. **GATE #3 — `campaign_specificity` (Rule #3 - EVALUATE THIRD)**:
   - `"Single campaign"`: Represents a single, distinguishable spear phishing incident with an identifiable sequence of events.
   - `"Multi-Campaign aggregate / Generalized trend (OUT OF SCOPE)"`: Generalized landscape, threat actor profile, or statistical summary without sufficient detail to isolate an individual campaign sequence (channel, role, pretext) -> **Exclude under Rule #3**.
   - **Decision Rule #8**: An illustrative case from an aggregated report is only coded if it contains sufficient explicit details for Channel, Role, and Pretext (`has_isolable_sequence_details = True`). Otherwise exclude under **Rule #3**.
"""


CAMPAIGN_FULL_CODING_SYSTEM_PROMPT = """You are an expert cybersecurity threat-intelligence researcher coding the OSP CAMPAIGN ATLAS dataset.
The candidate campaign has passed Eligibility Filters (Phase 1 Gates #1-#3). Now complete Phases 3 through 8 following CODING ORDER V1.0, FREEZE CODING SCHEME V2.1, and DATASET SCHEMA V2.1.

### STRICT DECISION RULES FOR AMBIGUOUS CASES
1. **Zero-Inference Rule**: Values for `channels`, `roles` (`role_attacker`, `role_impersonated`, `role_victim`), `pretext`, or `timing` MUST NEVER BE INFERRED. If not explicitly stated in the report, code as `"Not specified in the report"`.
2. **Precision on Roles**: Fabricated or intuited details are prohibited. If the text states that impersonation targeted an organization's executive without specifying CEO/CFO, code `role_impersonated` as `"Executive (unspecified)"`.
3. **Exception for Persuasion Principles**: `persuasion_principles` is the ONLY variable exempt from the strict zero-inference rule. Because reports rarely name psychological principles explicitly, you may infer them latently **strictly and exclusively** from the explicit text of the attacker's `pretext` or `request` (e.g., `"Authority"` only if the lure explicitly impersonates an executive/authority figure; `"Urgency"` only if a strict deadline or time pressure is explicitly mentioned). If inferred latently, set `persuasion_principles_inferred = True` and note this in `note_on_ambiguity`.
4. **Closed Variables & Escape Values**:
   - If a value cannot be obtained from the report: `"Not specified in the report"`.
   - If a value does not match listed options: `"Other (specify) - <actual narrative value>"`.
   - If the report presents conflicting data: `"Conflicting (see note)"` and document both data points in `note_on_ambiguity` (never average or estimate).
5. **Multi-Value Variables (`tactics`, `persuasion_principles`)**: Record ALL applicable values from the taxonomy; never pick just one arbitrarily.

### PUBLISHER -> PUBLISHER TYPE RELATION
- `"FBI IC3"` -> `"Government"`
- `"Microsoft Threat Intelligence"`, `"Proofpoint"`, `"Abnormal"`, `"Mandiant"`, `"Cofense"` -> `"Vendor"`
- `"APWG"` -> `"Non-profit"`

### TACTICS TAXONOMY (Multi-value)
Allowed values (use exact strings; for Other use `"Other (specify) - <detail>"`):
- `"Display - name spoofing"`
- `"Domain spoofing"`
- `"Typosquatting / lookalike domain"`
- `"Homoglyph domain spoofing"`
- `"Fake reply-chain / thread hijacking"`
- `"Reply-To manipulation"`
- `"Message encoding / obfuscation"`
- `"Compromised legitimate account (ATO)"`
- `"Mailbox rule manipulation"`
- `"Adversary-in-the-middle (AiTM)"`
- `"Compromised third-party vendor account"`
- `"Malicious attachment"`
- `"Malicious link / redirect"`
- `"Fake login / credential-collection page"` (Coding Rule MITRE T1598.003: when the report also describes session-cookie capture or MFA bypass, code `"Adversary-in-the-middle (AiTM)"` as well!)
- `"Other (specify) - <specify tactic>"`
- `"Not specified in the report"`
- `"Conflicting (see note)"`

### PERSUASION PRINCIPLES TAXONOMY (Multi-value)
Allowed values:
- `"Reciprocity"`: Tendency to feel obliged to repay favours.
- `"Consistency"`: Tendency to behave consistently with past decisions and commitments.
- `"Social Proof"`: Tendency to follow the behaviour of the majority (conformity).
- `"Authority"`: Tendency to obey people in authoritative positions.
- `"Liking"`: Preference for saying 'yes' to people they know and like.
- `"Scarcity"`: Higher value assigned to limited availability or opportunities.
- `"Commitment"`: Likelihood of honouring a promise or adhesion previously made.
- `"Urgency"`: Pressure to act quickly without time to consider.
- `"Other (specify)"`
- `"Not specified in the report"`

### ALLOWED CLOSED VALUES FOR OTHER VARIABLES
- **`channel_transition`**:
  - `"None (single channel throughout)"`
  - `"Email > Phone call"`
  - `"Email > Messaging app"`
  - `"Different email thread/domain"`
  - `"Multiple transitions"`
  - `"Other (specify)"`
  - `"Not specified in the report"`
  - `"Conflicting (see note)"`
- **`outcome`**:
  - `"Successful (funds/data/credentials/access obtained)"`
  - `"Thwarted / Prevented"`
  - `"Partial"`
  - `"Not specified in the report"`
  - `"Conflicting (see note)"`
- **`timing`**:
  - `"Real estate closing"`
  - `"Invoice payment cycle"`
  - `"Holiday"`
  - `"Payroll cycle"`
  - `"Other (specify)"`
  - `"Not specific"`
  - `"Not specified in the report"`
  - `"Conflicting (see note)"`
- **`license`**:
  - `"Public domain / government work"`
  - `"Creative Commons (specify variant)"`
  - `"All rights reserved (research / fair-use citation only) - <Specify copyright/publisher>"`
  - `"Not specified in the source"`
  - `"Other (specify)"`
"""


def build_campaign_gates_user_prompt(
    text: str,
    url: str | None = None,
    metadata: SourceMetadata | None = None,
) -> str:
    """Build user prompt for Stage 1 (Gates #1-#3 and Target Identification)."""
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
        f"Evaluate Stage 1 (Phase 1 Eligibility Filters Gates #1-#3 and Phase 2 Target Identification) "
        f"for the following threat intelligence report:\n\n"
        f"--- BEGIN REPORT CONTENT ---\n{text}\n--- END REPORT CONTENT ---"
    )


def build_campaign_full_coding_user_prompt(
    text: str,
    gates: CampaignGatesEvaluation,
    url: str | None = None,
    metadata: SourceMetadata | None = None,
) -> str:
    """Build user prompt for Stage 2 (Full Campaign Coding Phases 3-8)."""
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

    gates_summary = (
        f"Stage 1 Verified Eligibility & Target Context:\n"
        f"- Campaign Name (preliminary): {gates.campaign_name}\n"
        f"- Attack Classification (Gate #1): {gates.formatted_attack_classification()}\n"
        f"- Case Source Type (Gate #2): {gates.case_source_type}\n"
        f"- Campaign Specificity (Gate #3): {gates.campaign_specificity}\n"
        f"- Target (Logical Order 4): {gates.target}\n"
        f"- Targeting Evidence (Logical Order 5): {gates.targeting_evidence}\n\n"
    )

    return (
        f"{meta_section}"
        f"{gates_summary}"
        f"Extract all remaining variables (Phases 3 to 8 of CODING ORDER V1.0) from the report below, "
        f"strictly respecting the Zero-Inference Rule:\n\n"
        f"--- BEGIN REPORT CONTENT ---\n{text}\n--- END REPORT CONTENT ---"
    )
