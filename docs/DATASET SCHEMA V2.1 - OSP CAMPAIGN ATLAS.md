**DATASET SCHEMA V2.1 \- OSP CAMPAIGN ATLAS**  
**Version:** 2.1  
**Date:** 2026-10-26  
**Coding schema reference:** FREEZE CODING SCHEMA V2.1 (2026-10-26). The definition of “*Pure Spear Phishing (Targeted lure \+ Impersonation)*” was corrected.  
**Supersedes:** DATASET SCHEMA V2 (2026-10-18). JSON variables and the definition of “*Pure Spear Phishing (Targeted lure \+ Impersonation)*” were corrected.

**Transversal Rule (applies in almost all cases).**  
Unless otherwise indicated, each closed-value variable must also accept the following responses:

* **Not specified in the report**: Used when the value cannot be obtained from the document / source. Value for a channel, role, pretext or timing must never be inferred.   
* **Other (specify)** : The actual value must be detailed in narrative form, accompanied by a note.  
* **Conflicting (see note)** : both data points are documented, and the explanation goes in the “note\_on\_ambiguity” variable. No averaging or estimation.

If a campaign has more than one valid value in a single variable (multi-value variables), all applicable values must be recorded.

**Exception:** The “*persuasion\_principles*” variable may be inferred latently, but strictly and exclusively from the explicit text of attacker’s pretext request (e.g., Authority only if the lure explicitly impersonates an executive; Urgency only if a strict deadline is mentioned)

**Definitions.**  
**Unit of Analysis:** In the Campaigns table, each row is one individual, publicly reported Organizational Spear Phishing (OSP) campaign. In the Reports table, each row is one aggregated report that compiles OSP (including BEC) statistics over specific period and geographic region.

**OSP Campaign:** Organizational Spear Phishing campaigns are defined as incidents in which an attacker selects a specific organization, or a specific group or role within it, as the target and uses a tailored deceptive communication, typically involving impersonation of trusted person, role, organization, or service, to induce a member of the target organization to take an action (transfer funds, disclose credentials or data, open or execute a payload, or grant access) that advances fraud against or compromise of that organization. For the purposes of this research, campaigns must present a structured and identifiable sequence of events (e.g., Impersonation → Fraudulent request / Tailored lure → Payload → Access).

**BEC:** A subtype of organizational spear phishing in which the attacker’s objective is financial or confidential-information fraud through impersonation of vendor/supplier information or internal personnel.

**OSP Report:** Aggregated reports are documents published by institutions or vendors that compile statistical and macroeconomic information regarding Organizational Spear Phishing and BEC (such as incident volume, credential compromised rates, or cumulative financial losses) corresponding to a specific geographic region and time period.

**Scope**

| IN SCOPE | OUT OF SCOPE |
| :---- | :---- |
| BEC campaigns | Mass or opportunistic delivery with no evidence of target selection |
| Targeted spear phishing against an organization that uses impersonation (of a person, role, organization, or service) to deliver a payload, harvest credentials, or obtain access. | Phishing aimed at consumers or the general public rather than an organization. |
| Targeted campaigns attributed to APT or espionage actors, when the report shows the organization or its personnel were deliberately selected and a tailored lure with impersonation was used. | Campaigns where impersonation is not part of the attack path. |
|  | Generalized trends without an isolable sequence of events. |

**Test for targeting:** At least one explicit piece of evidence in the report that the organization, sector segment, or role was deliberately selected (named victim organization, victim list or sector-specific targeting, role-specific recipients, personalized/tailored lure content). If the report gives no such evidence, code the targeting evidence as “Not specified in the report” and exclude under Rule 1\.  
**Mandatory evaluation order \- Exclusion rules:**

1. **Rule \#1 \- attack\_classification**  
   1. Exclude immediately if the campaign shows no evidence of target selection (“No target selection (OUT OF SCOPE)”) or impersonation is not part of the attack path (“Impersonation unnecessary (OUT OF SCOPE)”). Credential theft is not excluded by itself: it is in scope when the campaign is targeted at an organization and uses impersonation. It is out of scope only when it is untargeted or involves no impersonation, even if the report labels it “BEC” or “spear phishing”.  
2. **Rule \#2 \- case\_source\_type**  
   1. If the campaign is not based on a real-life case, it is excluded.  
3. **Rule \#3 \- campaign\_specificity**  
   1. If the campaign is not a specific case or is a generalized trend without a distinguishable sequence, it is excluded.  
      

**Campaign Dataset Schema**  
**Analysis unit:** One public, individual OSP campaign report.

**Table**

| Field | Type | Allowed values | Mandatory |
| :---- | :---- | :---- | :---- |
| campaign\_id | string (unique) | Auto-generated | YES |
| campaign\_name | string (free text) | Open response | YES |
| publisher | categorical | Microsoft Threat Intelligence Proofpoint Abnormal Mandiant Cofense APWG FBI IC3 Other (specify) Not specified in the report Conflicting (see note)  | YES |
| publisher\_type | categorical (derived from “publisher”) | Government Vendor Academic Non-profit Other (specify) Not specified in the report Conflicting (see note) | YES |
| publication\_date | date (YYYY-MM-DD) | YYYY-MM-DD format Other (specify) Not specified in the report Conflicting (see note) | YES |
| case\_source\_type | categorical \- excluded rules \#2 | Standalone campaign report Illustrative case within aggregate report Non-real life case (OUT OF SCOPE) | YES |
| campaign\_specificity | categorical \- excluded rules \#3 | Single campaign Multi-Campaign aggregate / Generalized trend (OUT OF SCOPE) | YES |
| attack\_classification | categorical \- exclusion rule \#1: evaluate first | Pure BEC (Impersonation \+ Fraud) Pure Spear Phishing (Targeted lure \+ Impersonation) Hybrid Campaign \- Targeting and impersonation necessary (other vector \- specify) Impersonation unnecessary (OUT OF SCOPE) No target selection (OUT OF SCOPE)  | YES |
| targeting\_evidence | string (free text) | Open response Not specified in the report Conflicting (see note) | YES |
| outcome | categorical | Successful (funds/ data/credentials/access obtained) Thwarted / Prevented  Partial Not specified in the report Conflicting (see note) | YES |
| target | string (free text) | Open response | YES |
| channels | string (free text, descriptive)  | Open response | YES |
| channel\_transition | categorical | None (single channel throughout) Email \> Phone call Email \> Messaging app Different email thread/domain Multiple transitions Other (specify) Not specified in the report Conflicting (see note) | YES |
| tactics | categorical (multiple values supported \- rule \# 5\) | Display \- name spoofing Domain spoofing Typosquatting / lookalike domain Homoglyph domain spoofing Fake reply-chain / thread hijacking Reply-To header manipulation Message encoding / obfuscation Compromised legitimate account (ATO) Mailbox rule manipulation Adversary-in-the-middle (AiTM) Compromised third-party vendor account Malicious attachment Malicious link / redirect Fake login / credential-collection page Other (specify) Not specified in the report Conflicting (see note) | YES |
| role\_attacker | string (free text, subfield of roles) | Open response | YES |
| role\_impersonated | string (free text, subfield of roles) | Open response | YES |
| role\_victim | string (free text, subfield of roles) | Open response | YES |
| request | string (free text) | Open response | YES |
| pretext | string (free text) | Open response | YES |
| persuasion\_principles | categorical (multiple values supported) | Reciprocity Consistency Social Proof Authority Liking Scarcity Commitment Urgency Other (specify) Not specified in the report | YES |
| timing | categorical | Real estate closing Invoice payment cycle Holiday Payroll cycle Other (specify) Not specific Not specified in the report Conflicting (see note) | YES |
| impact | string (free text) | Open response | YES |
| information\_website | string (URL) | Web link | YES |
| coding\_date | datetime with timezone | ISO 8601 \- Coordinated Universal Time “Zulu” (YYYY-MM-DDThh:mm:ssZ) | YES |
| coder | categorical | Human coded LLM assisted Human verified Dual coded | YES |
| license | categorical | Public domain / government work Creative Commons (specify variant) All rights reserved (research / fair-use citation only) \- Specify Not specified in the source Other (specify) | YES |
| note\_on\_ambiguity | string (free text) | Open response | NO |
| agreement\_rate | integer  | 0% \- 100% N/A (Default unless Coder is “*Dual coded*”) | NO |

**Campaign JSON format \- Human Coded Schema**

```json
{
    "campaign_id": "",
    "campaign_name": "",
    "publisher": "",
    "publisher_type": "",
    "publication_date": "",
    "case_source_type": "",
    "campaign_specificity": "",
    "attack_classification": "",
    "targeting_evidence": "",
    "outcome": "",
    "target": "",
    "channels": "",
    "channel_transition": "",
    "tactics" : [
        ""
    ],
    "roles": {
        "role_attacker": "",
        "role_impersonated": "",
        "role_victim": ""
    },
    "request": "",
    "pretext": "",
    "persuasion_principles": [
        ""
    ],
    "timing": "",
    "impact": "",
    "information_website": "",
    "coding_date": "",
    "coder": "",
    "license": "",
    "note_on_ambiguity": "",
    "agreement_rate": ""
    
}
```

**Attack classification: Value definitions.**

| Value | Definition |
| :---- | :---- |
| Pure BEC (Impersonation \+ Fraud) | Targeted impersonation of a vendor/supplier or internal personnel whose objective is to obtain funds, or confidential information requested through the impersonation itself, by a direct request. No other attack vector is required beforehand. |
| Pure Spear Phishing (Targeted lure \+ Impersonation) | Targeted, tailored lure involving impersonation of a person, role, organization, or service that leads to credential disclosure, payload execution, data theft, or access. No other attack vector is required beforehand. Objectives that are BEC are classified as “*Pure BEC*” |
| Hybrid Campaign \- Targeting and impersonation necessary (other vector \- specify) | Another attack vector (e.g., AiTM, SEO poisoning / malvertising, compromised infrastructure) is necessary before or alongside the targeted impersonation to carry out the objective. This value takes precedence over the two Pure values. The additional vector(s) must be named in the row; the attacker’s final objective is recorded in “*Request*” and “*Impact*”. |
| Impersonation unnecessary (OUT OF SCOPE) | Impersonation is not part of the attack path. |
| No target selection (OUT OF SCOPE) | No evidence of the target selection (mass or opportunistic delivery). See “*Test for targeting*” |

**Precedence:** In the event that stolen credentials are obtained at some stage of the attack and are subsequently used to carry out a fraudulent request (e.g., payroll diversion), the campaign is coded as “*Hybrid*” only if an additional vector was required to reach that stage; otherwise it is classified by its final objective.

**Persuasion principle(s) taxonomy**

| Principle | Definition (summary) |
| :---- | :---- |
| Reciprocity | Tendency to feel obliged to repay favours. |
| Consistency | Tendency to behave consistently with past decisions and behaviours. |
| Social Proof / Conformity | Tendency to follow the behaviour of the majority. |
| Authority | Tendency to obey people in authoritative positions. |
| Liking | Preference for saying “yes” to people they know and like. |
| Scarcity | Higher value assigned to limited availability or opportunities. |
| Commitment | Likelihood of honouring a promise or adhesion previously made. |
| Urgency | Pressure to act quickly without time to consider. |

**Tactics taxonomy**

| Tactic Name | Definition | Example |
| :---- | :---- | :---- |
| Display \- name spoofing | “This scheme uses the name of the spoofed executive in the ‘From’ Field. But the email address actually comes from an outside service such as Gmail that belongs to the attacker.” (Proofpoint, 2020\) | Real case. From: “Jane Smith” \<jane.smith@company.com\> Spoof case. From: “Jane Smith” \<j.smith8847@gmail.com\> |
| Domain spoofing | “This tactic involves an attacker hijacking your domain to send fraudulent emails to your employees, partners and customers. Attackers exploit the trust people place in your company brand name to steal money and valuable information.” (Proofpoint, 2020\) | Spoof case:  The fraudulent email is sent from the exact legitimate domain (e.g., From: “CEO” \<ceo@yourcompany.com\>) because the attacker exploits the lack of email authentication controls (like DMARC) on the victim’s domain. |
| Lookalike domains | In this scheme, “the attacker registers a domain that looks confusingly similar to a trusted legitimate domain.” (Proofpoint, 2020\) | Real case: ‘legitcompany.com’, Spoof case: ‘legtcompany.com’   |
| Reply-To manipulation | “Another tactic adopted by attackers is to use a faked organisation’s true domain in the ‘From’ address box. Adding another domain to the ‘Reply-To’ address box tricks the users into thinking they have received a reply. A reply to a field controlled by the attacker results in a reply being sent back to the attacker.” (Atlam, H. F., & Oluwatimilehin, O., 2023\) | Spoof case: From: billing@legit.com Reply-To: billing-legit@attacker.com |
| Message encoding / obfuscation | “To avoid being detected by email gateways, BEC attackers sometimes utilise encoding ploys that alter the characters in the message. When a BEC message is opened in the email account of a client, it seems to be a regular email. A hex editor scan, on the other hand, reveals the real colours of the image.” (Atlam, H. F., & Oluwatimilehin, O., 2023\) | Spoof case: Using zero-width spaces or homoglyphs in the email body so security filters read “I n v o i c e” while the human eye reads “Invoice”. |
| Adversary-in-the-middle (AiTM). | A technique where an attacker deploys a proxy server between a user and a legitimate service to intercept credentials and session cookies, bypassing multi-factor authentication (MFA). (Microsoft Threat Intelligence, 2023\) | Real case: The victim clicks a phishing link and logs into a fake Microsoft 365 page. The proxy captures their session cookie, allowing the attacker to bypass MFA and access the account. |
| Compromised legitimate account (ATO). | Account Takeover (ATO) occurs when an attacker gains unauthorized access to a legitimate employee’s email account and uses it to conduct fraudulent activities from within the organization. (FBI IC3, 2025\) | Real case: An attacker logs into the CFO’s actual email account using stolen credentials and sends an email to the finance department requesting a wire transfer. The email passes all authentication checks because it is genuine. |
| Mailbox rule manipulation. | The unauthorized creation or modification of email inbox rules by an attacker who has compromised an account, designed to conceal malicious communications from the victim. (Patterson, 2026\) | Real case: An attacker creates an Outlook rule that automatically moves any incoming email containing the words “fraud” or “bank” to the “RSS Feeds” or “Deleted Items” folder so the victim never sees security warnings. |
| Compromised third-party vendor account. | Also known as Vendor Email Compromise (VEC). An attacker compromises the email account of a trusted supplier and uses that established trust to request fraudulent payments from the vendor’s customers. (Abnormal Security) | Real case: An attacker breaches a logistics supplier’s email account and sends an email to all of their clients stating: “Our bank details have changed, please send all future payments to this new account.” |
| Malicious attachment | A tailored message carries a file (e.g., an Office document, executable, PDF, or archive) that delivers malware or gives the attacker access once the victim opens it. It differs from other forms of spearphishing in that it relies on malware attached to the message. (MITRE ATT\&CK, T1566.001)  | Illustrative case: A finance employee receives a message that appears to come from a known supplier with an attached archive; opening the file runs a loader on the employee’s device.  |
| Malicious link / redirect | A tailored message contains a link that sends the victim to an attacker-controlled resource (e.g., a file download or an intermediate page) in order to gain access to the victim’s systems, instead of carrying a file itself. (MITRE ATT\&CK, T1566.002)  | Illustrative case: An email posing as a business partner includes a link that redirects through an intermediate page to a download hosted on attacker infrastructure.  |
| Fake login / credential-collection page | A tailored message directs the victim to a web page that imitates a legitimate login or portal so that the credentials entered are captured by the attacker. Coding rule: when the report also describes session-cookie capture or MFA bypass, “Adversary-in-the-middle (AiTM)” is coded as well. (MITRE ATT\&CK, T1598.003) | Illustrative case: A link in an email posing as the organization’s IT department opens a page copying the company’s single sign-on screen; the submitted credentials go to the attacker.  |

**Reports Dataset Schema**  
**Analysis Unit:** One aggregated report that compiles OSP (including BEC) statistics such as incident volume, credential compromise rates or cumulative financial losses over a specific period and region.

**Table**

| Field | Type | Allowed values | Mandatory |
| :---- | :---- | :---- | :---- |
| report\_id | string (unique) | Auto-generated | YES |
| report\_name | string (free text) | Open response | YES |
| report\_type | categorical | Trimestral Landscape Annual Other (specify) Not specified in the report Conflicting (see note) | YES |
| period\_report | categorical | Annual Q1 Q2 Q3 Q4 Other (specify) Not specified in the report Conflicting (see note) | YES |
| report\_year | integer (YYYY) | YYYY format Other (specify) Not specified in the report Conflicting (see note) | YES |
| geographic\_scope | categorical | Global  U.S. Other (specify) Not specified in the report Conflicting (see note) | YES |
| publisher | categorical | FBI IC3 Microsoft APWG Proofpoint Abnormal Mandiant Cofense Other (specify) Not specified in the report Conflicting (see note) | YES |
| publisher\_type | categorical (derived from “publisher”) | Government Vendor Academic Non-profit Other (specify) Not specified in the report Conflicting (see note) | YES |
| data\_source | categorial | Self-reported victims Vendor customer telemetry Other (specify) Not specified in the report Conflicting (see note) | YES |
| incident\_counts | Integer | Other numeric response (integer) Not specified in the report Conflicting (see note) | YES |
| financial\_loss | string (currency \+ amount) | Other numeric response (USD or other currency) Not specified in the report Conflicting (see note) | YES |
| information\_website | string (URL) | Web link | YES |
| coding\_date | datetime with timezone | ISO 8601 \- Coordinated Universal Time “Zulu” (YYYY-MM-DDThh:mm:ssZ) | YES |
| coder | categorical | Human coded LLM assisted Human verified Dual coded | YES |
| license | categorical | Public domain / government work  Creative Commons (specify variant) All rights reserved (research / fair-use citation only) \- Specify Not specified in the source Other (specify) | YES |
| note\_on\_ambiguity | string (free text) | Open response | NO |
| agreement\_rate | integer | 0% \- 100% N/A (Default unless Coder is ‘*Dual coded*’) | NO |

**Report JSON format \- Human Coded Schema**

```json
{
    "report_id": "",
    "report_name": "",
    "report_type": "",
    "period_report": "",
    "report_year": "",
    "geographic_scope": "",
    "publisher": "",
    "publisher_type": "",
    "data_source": "",
    "incident_counts": "",
    "financial_loss": "",
    "information_website": "",
    "coding_date": "",
    "coder": "",
    "license": "",
    "note_on_ambiguity": "",
    "agreement_rate": ""

}
```

**Exclusion Log Schema**  
A separate sheet, outside the dataset tables, with one row per candidate excluded under Rules \#1 to \#3.

| Variable | Type | Possible results |
| :---- | :---- | :---- |
| excluded\_id | string (unique) | Auto-generated |
| campaign\_name | string (free text) | Name as given in the report |
| publisher  | categorical | Same values as the Publisher variable |
| information\_website | string (URL) | Web link |
| rule\_triggered | categorical | Rule \#1 Rule \#2 Rule \#3 |
| exclusion\_reason | string (free text) | Concrete sentence justifying the exclusion against the written definition |
| exclusion\_date | datetime with timezone | ISO 8601 \- Coordinated Universal Time “Zulu” (YYYY-MM-DDThh:mm:ssZ) |
| evaluator | string (free text) | Name or initials of the person who made the decision |

**Decision Rules for Ambiguous Cases**

* Never infer channel, role, pretext or timing; if absent, code “*Not specified in the report*”. Persuasion principles are the only exception (see Transversal Rule).  
* If a closed variable has a value that does not match any listed option, code “*Other (specify)*” and describe it.  
* If a campaign has more than one valid value, record all of them.  
* If a source reports conflicting data, document both data points. If the conflict is unresolvable, explain it in “*note\_on\_ambiguity*”.  
* An ambiguity not covered by the rules must be documented in “*note\_on\_ambiguity”* and in the decision log, to serve as precedent.  
* A closed category must not change halfway through core coding. If it does, record it in the decision log and re-evaluate rows already coded.  
* The “*agreement\_rate*” must be “*N/A*” unless the coder is “*Dual coded*”. A numeric score (0% \- 100%) is calculated only for Dual coded rows.  
* **Dual coded requires independence:** the second coder must not see the first coder’s values or the LLM first-pass output. Each coder’s original values are preserved in a separate sheet and discrepancies are recorded before reconciliation. A human verifying an existing LLM output is “*Human verified*”, not “*Dual coded*”.