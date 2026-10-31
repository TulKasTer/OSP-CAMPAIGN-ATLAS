# CODING ORDER V1.0
**Version:** 1.0  
**Date:** 2026-10-30  
**Coding schema reference:** FREEZE CODING SCHEMA V2.1 (2026-10-26).\
**Dataset schema reference:** DATASET SCHEMA V2.1 (2026-10-26).

## Explanation of the Logical Order for Campaign Coding

The proposed logical order reorganizes the variables according to the natural evaluation and coding flow of a cybersecurity incident, prioritizing exclusion criteria (gates) before investing time in extracting tactical details.

- **Phase 1: Eligibility Filters (1-3):** The gates are evaluated to determine whether the campaign is valid, its source, and its specificity before proceeding.
- **Phase 2: Target Identification (4-5):** Defines whom the attack is directed at and the evidence supporting that conclusion.
- **Phase 3: Identity and Sources (6-11):** Groups the basic metadata (ID, name, publisher, dates, and reference links).
- **Phase 4: Involved Actors (12-14):** Identifies the three roles (attacker, impersonated role, and victim).
- **Phase 5: Vectors and Execution (15-17):** Details the communication channels used, transitions between them, and general tactics.
- **Phase 6: Social Engineering (18-20):** Breaks down the central deception through the pretext used, the final request, and the persuasion principles.
- **Phase 7: Outcomes (21-23):** Documents whether the attack succeeded, its final impact, and when it occurred.
- **Phase 8: Auditing and Quality (24-28):** Collects administrative data about who coded the row, review dates, identified ambiguities, and the percentage of agreement between analysts.

### Structured Table

| Logical Order | Original Order | Field (Variable) | Description | Type / Rules |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 8 | Attack Classification - GATE #1 | Specifies whether the campaign is a pure BEC campaign, a pure (non-BEC) spear phishing campaign, or another classification. | Dropdown - EVALUATE FIRST |
| 2 | 6 | Case Source Type - GATE #2 | Specifies whether the campaign was obtained from a standalone campaign report or extracted from an aggregate report. | Dropdown - EVALUATE SECOND |
| 3 | 7 | Campaign Specificity - GATE #3 | Specifies whether the entry represents a single, distinguishable spear phishing incident. | Dropdown - EVALUATE THIRD |
| 4 | 11 | Target | The specific demographic, industry, or region the attacker is targeting. | String - Open response |
| 5 | 9 | Targeting Evidence | The explicit evidence in the report that the organization, sector segment, or role was deliberately selected. | String - Open response / escape value |
| 6 | 1 | Campaign ID | Unique campaign identifier. | Auto, unique (CMP-0001) |
| 7 | 2 | Campaign Name | Name by which the campaign is known. | String - Open response |
| 8 | 3 | Publisher | Auditor or organization(s) publishing the public report. | Dropdown |
| 9 | 4 | Publisher Type | The type of institution publishing the report. | Dropdown |
| 10 | 5 | Publication Date | The date on which the campaign report was published. | YYYY-MM-DD / escape value |
| 11 | 23 | Information Website | The URL or source of the threat intelligence report used for the analysis. | Web link |
| 12 | 15 | Roles - Attacker | Identifies the attacker. | String - Open response |
| 13 | 16 | Roles - Impersonated Role | Identifies the role impersonated by the attacker. | String - Open response |
| 14 | 17 | Roles - Victim | Identifies the victim of the attack. | String - Open response |
| 15 | 12 | Channels | The communication medium or technical vector used to execute the attack. | String - Open response |
| 16 | 13 | Channel Transition | The path through which the attack is carried out across different media. | String - Open response |
| 17 | 14 | Tactics | Specific social-engineering or technical techniques used to execute the attack, independent of the channel. | Multi-value (one per line) |
| 18 | 19 | Pretext | The fabricated story or social-engineering lure used by the attacker to manipulate the victim. | String - Open response |
| 19 | 18 | Request | The final action the attacker wants the victim to perform. | String - Open response |
| 20 | 20 | Persuasion Principle(s) | The psychological or social-engineering principle(s) that the attacker leverages within the pretext. | Multi-value (one per line) |
| 21 | 10 | Outcome | Whether the attack succeeded in achieving its objective (funds, data, credentials, or access). | Dropdown |
| 22 | 22 | Impact | The final consequence or damage caused by the attack. | String - Open response |
| 23 | 21 | Timing | The specific moment or point in the victim’s business process or calendar at which the attack was executed. | Dropdown |
| 24 | 26 | License | The usage license or terms of use declared by the source report’s publisher. | Dropdown |
| 25 | 25 | Coder | Specifies the provenance of this row’s coding: whether it was produced by an unverified LLM-assisted first pass, verified by a human after LLM assistance, or independently coded by two analysts for inter-rater comparison. | Dropdown |
| 26 | 24 | Coding Date | The date and time at which this row was coded or entered into the dataset. | ISO 8601 - Zulu |
| 27 | 27 | Note on Ambiguity | Any situation where the report does not provide sufficient information or presents contradictory information. | String - Open response |
| 28 | 28 | Agreement Rate | Percentage agreement for this row between two independent analysts. Default rule: must be “N/A” unless “Coder” is “Dual coded”. | String - N/A or percentage |


## Explanation of the Logical Order for Report Coding

To organize this aggregate-report coding schema logically, it can be structured into four sequential phases, ranging from general identification of the threat intelligence document to metric extraction and final quality control.

- **Phase 1: Identification and Scope:** Defines the document’s essential metadata (ID, name, type, period, and geographic region).
- **Phase 2: Authorship and Sources:** Groups the report’s provenance, the source of the underlying data, reference links, and usage license.
- **Phase 3: Quantitative Findings:** Isolates the main extracted metrics (incident counts and financial losses associated with BEC/spear phishing).
- **Phase 4: Auditing and Quality:** Centralizes administrative variables to ensure inter-rater reliability (dates, coder provenance, notes about ambiguities in the figures, and agreement rate).

### Structured Table

| Logical Order | Field (Variable) | Description | Format / Allowed Values |
| :--- | :--- | :--- | :--- |
| 1 | Report ID | Unique report identifier. | Auto, unique (REP-0001) |
| 2 | Report Name | Name by which the report is known. | String - Open response |
| 3 | Report Type | Type of report. | Dropdown |
| 4 | Period Report | Period covered by the report. | Dropdown |
| 5 | Report Year | Year of the report. | YYYY / escape value |
| 6 | Geographic Scope | Geographic area covered by the report. | Dropdown |
| 7 | Publisher | Auditor or organization(s) publishing the public report. | Dropdown |
| 8 | Publisher Type | The type of institution publishing the report. | Dropdown |
| 9 | Data Source | How the data was obtained. | Dropdown |
| 10 | Information Website | The URL or source of the threat intelligence report used for the analysis. | Web link |
| 11 | License | The usage license or terms of use declared by the source report’s publisher. | Dropdown |
| 12 | Incident Counts | Number of incidents reported. | Integer |
| 13 | Financial Loss | Amount of money reported as losses related to targeted phishing (BEC / spear phishing). | String (currency + amount) |
| 14 | Coder | Specifies the provenance of this row’s coding: whether it was produced by an unverified LLM-assisted first pass, verified by a human after LLM assistance, or independently coded by two analysts for inter-rater comparison. | Dropdown |
| 15 | Coding Date | The date and time at which this row was coded or entered into the dataset. | ISO 8601 - Zulu |
| 16 | Note on Ambiguity | Any situation where the aggregate report does not clearly indicate whether a figure corresponds exclusively to BEC or to broader OSP, does not specify how the data was obtained, or presents figures that overlap with other categories in the same report. | String - Open response |
| 17 | Agreement Rate | Percentage agreement for this row between two independent analysts: the number of compared variables with identical values divided by the number of variables compared. Cohen’s κ is computed per variable across the dual-coded sample and reported in the coding and agreement protocol, not stored in this row. | String - N/A or percentage; N/A unless Dual coded |