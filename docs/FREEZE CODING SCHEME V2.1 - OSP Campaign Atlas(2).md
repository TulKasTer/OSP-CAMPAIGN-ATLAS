**FREEZE CODING SCHEMA V2.1 \- OSP CAMPAIGN ATLAS**  
**Version:** 2.1  
**Date:** 2026-10-26  
**Supersedes:** FREEZE CODING SCHEMA V2 (2026-10-15). Empty fields in the table were completed, and the definition of “*Pure Spear Phishing (Targeted lure \+ Impersonation)*” was corrected.

**Definition of Unit of Analysis**  
In the case of the campaigns table, each row represents an individual, publicly reported campaign. On the other hand, in the reports table, each row represents an individual report that compiles information about Organizational Spear Phishing (including BEC) over a specific time period.

**Campaign Definition**  
Organizational Spear Phishing campaigns are defined as incidents in which an attacker selects a specific organization, or a specific group or role within it, as the target and uses a tailored deceptive communication, typically involving impersonation of trusted person, role, organization, or service, to induce a member of the target organization to take an action (transfer funds, disclose credentials or data, open or execute a payload, or grant access) that advances fraud against or compromise of that organization. For the purposes of this research, campaigns must present a structured and identifiable sequence of events (e.g., Impersonation → Fraudulent request / Tailored lure → Payload → Access).   
Business Email Compromise (BEC) is a subtype of organizational spear phishing in which the attacker’s objective is financial or confidential-information fraud through impersonation of vendor/supplier information or internal personnel.

**Report Definition**  
Aggregated reports are documents published by institutions or vendors that compile statistical and macroeconomic information regarding Organizational Spear Phishing and BEC (such as incident volume, credential compromised rates, or cumulative financial losses) corresponding to a specific geographic region and time period.

**Define Scope**

| IN SCOPE | OUT OF SCOPE |
| :---- | :---- |
| BEC campaigns | Mass or opportunistic delivery with no evidence of target selection |
| Targeted spear phishing against an organization that uses impersonation (of a person, role, organization, or service) to deliver a payload, harvest credentials, or obtain access. | Phishing aimed at consumers or the general public rather than an organization. |
| Targeted campaigns attributed to APT or espionage actors, when the report shows the organization or its personnel were deliberately selected and a tailored lure with impersonation was used. | Campaigns where impersonation is not part of the attack path. |
|  | Generalized trends without an isolable sequence of events. |

**Test for targeting:** At least one explicit piece of evidence in the report that the organization, sector segment, or role was deliberately selected (named victim organization, victim list or sector-specific targeting, role-specific recipients, personalized/tailored lure content). If the report gives no such evidence, code the targeting evidence as "Not specified in the report" and exclude under Rule 1\.

**Excluded Rules for Campaign Table.**

1. The first variable to be evaluated must be "*Attack Classification*", before the rest of the variables in the row. If the campaign shows no evidence of target selection (mass or opportunistic delivery), or impersonation is not part of the attack path, the campaign must be immediately excluded ("*No target selection (OUT OF SCOPE)*" or "*Impersonation unnecessary (OUT OF SCOPE)*") and logged in the Exclusion Log with its reason. Credential theft is not excluded by itself: it is in scope when the campaign is targeted at an organization and uses impersonation. It is out of scope only when it is untargeted or involves no impersonation, even if the report labels it as “*BEC*” or “*spear phishing*”.  
2. The second variable to be evaluated must be “*Case Source Type*”, after the check of the variable “*Attack Classification*”. This is because, if the campaign isn’t based on a real-life case, the campaign must be immediately excluded, making it pointless to complete the remaining variables.  
3. The third variable to be evaluated must be “*Campaign Specificity*”, after the check of the variable “*Case Source Type*”. This is because each row in this table must represent a single, distinguishable spear phishing campaign with its own sequence of events. If the report presents generalized trends without sufficient detail to isolate an individual sequence (channel, role, pretext), the entry must be excluded from this table.

**Exclusion Log**  
A separate sheet, outside the dataset tables, with one row per candidate excluded under Rules 1 to 3\.

| Variable | Definition | Possible results | Example |
| :---- | :---- | :---- | :---- |
| Excluded ID | Unique excluded campaign identifier  | identifier	Auto-generated, unique per row | EXC-0002 |
| Campaign Name | Name of the excluded campaign, as given in the report | Open response | Drive-by download campaign leveraging EtherHiding and ClickFix to deliver Lumma |
| Publisher  | Auditor or Organization(s) publishing the public report. | Same values as the Publisher variable | Microsoft Threat Intelligence |
| Information Website | The URL or source of the threat intelligence report used for the analysis. | Web link | [https\://www\.microsoft.com/en-us/security/blog/2025/05/21/lumma-stealer-breaking-down-the-delivery-techniques-and-capabilities-of-a-prolific-infostealer/](https://www.microsoft.com/en-us/security/blog/2025/05/21/lumma-stealer-breaking-down-the-delivery-techniques-and-capabilities-of-a-prolific-infostealer/)  |
| Rule Triggered | Rule under which the campaign was excluded | Rule \#1 Rule \#2 Rule \#3 | Rule \#1 |
| Exclusion Reason | Concrete sentence that justifies the exclusion against the written definition | Open response | The campaign relies on opportunistic drive-by download via compromised websites and mass delivery of fake CAPTCHA lures, with no explicit evidence of deliberate target selection against a specific organization or role. |
| Exclusion Date | The date and time at which the exclusion was decided | ISO 8601 \- Coordinated Universal Time “Zulu” (YYYY-MM-DDThh:mm:ssZ) | 2026-10-22T07:23:56Z |
| Evaluator | Person who made the exclusion decision | Open response (name or initials) | JFBV |

**Decision Rules for Ambiguous Cases.**

1. The values for channel, role, pretext, or timing data must never be inferred. If these do not appear explicitly within the report, they must be coded as “*Not specified in report*”. **Exception**: Persuasion principles are exempt from the strict zero-inference rule. Because threat intelligence reports rarely label psychological tactics explicitly, persuasion principles may be inferred latently. However, this inference must be strictly and exclusively grounded in the explicit text of the attacker’s pretext or fraudulent request (e.g., inferring “*Authority*” only if the lure explicitly involves impersonating an executive, or “*Urgency*” if a strict deadline is mentioned).  
2. The value “*Not specified*” is a valid entry used to avoid leaving empty cells and to symbolize that the variable’s value cannot be obtained from the document’s information.  
3. Codings must be precise and preserve details; fabricated or intuited information is not allowed. If the text states that the impersonation targeted an organization’s executive, it cannot be assumed that it is the CEO/CFO; in this case, it must be coded as “*Executive (unspecified)*”.   
4. If a closed variable has a value that does not exactly match one of the listed options, it must be coded as “*Other (specify)*”, and the actual value must be detailed in narrative form.  
5. If a campaign has more than one valid value for a single variable, all applicable values must be recorded; a single value must not be chosen arbitrarily.  
6. If a source reports conflicting data for the same incident, both data points must be documented, and neither should be arbitrarily discarded.  
7. If the information conflict is unresolvable, mark the row with a  “*Note in Ambiguity*” explaining the conflict, and do not attempt to force a single result (e.g., through averaging or estimation).  
8. An illustrative case from an aggregated report is only coded if it contains sufficient details for Channel, Role and Pretext.  
9. A closed category must not be changed halfway through the Core coding process. If a change is made, it must be recorded in the decision log, and the rows already coded under the previous category must be re-evaluated.  
10. If an ambiguity does not clearly fall under any of the previous rules, it must be documented in the “*Note on Ambiguity*” for that row and also recorded in the decision log. This will serve as a precedent to prevent falling into the same ambiguity should a similar situation arise in the future.  
11. The default value for the “*Agreement rate*” variable must strictly be “*N/A*”. A numeric score (0% \- 100%) must only be calculated, assigned, and recorded if the “Coder” variable is explicitly marked as “*Dual coded*” (indicating the row was independently analyzed by two distinct researchers \- LLM & Human, or Human & Human).  
12. A row may be marked “*Dual coded*” only if the two codings were independent: the second coder must not see the first coder’s values, nor the LLM first-pass output, before coding. Each coder’s original values are preserved in a separate sheet, and discrepancies are recorded before any discussion or reconciliation. A row where a human verifies an existing LLM output is “*Human verified*”, not “*Dual coded*”.

**Campaign variables definitions**

* **“*Publisher*” and “*Publisher Type*” relation.**  
  * The following table defines the specific value that must be assigned to the 'Publisher Type' variable depending on the Publisher.

| Publish Type | Publisher |
| :---- | :---- |
| Government | FBI IC3. |
| Vendor | Microsoft Threat Intelligence. Proofpoint. Abnormal. Mandiant. Cofense |
| Non-Profit | APWG |

    

* **Persuasion principle(s) taxonomy.**  
  * The following table containing definitions and phishing examples of persuasion principles was extracted in its entirety from the paper *‘Cognitive Triaging of Phishing Attacks*’ by Van Der Heijden, A., & Allodi, L. (2019).

| Principle | Definition | Phishing text example |
| :---- | :---- | :---- |
| Reciprocity | “Tendency to feel obliged to repay favours from others. “I do something for you, you do something for me.” (Van Der Heijden, A., & Allodi, L., 2019\) | “While we work hard to keep our network secure, we’re asking you to help us keep your account safe.” (Van Der Heijden, A., & Allodi, L., 2019\) |
| Consistency | “Tendency to behave in a way consistent with past decisions and behaviours. After committing to a certain view, company or product, people will act in accordance with those commitments.” (Van Der Heijden, A., & Allodi, L., 2019\) | “You agreed to terms and conditions before using our service, so we ask you to stop all activities that violate them. Click here to unflag your account for suspension.” (Van Der Heijden, A., & Allodi, L., 2019\) |
| Social Proof / Conformity | “Tendency to reference the behaviour of others, by using the majority behaviour to guide their own actions.” (Van Der Heijden, A., & Allodi, L., 2019\) | “We are introducing new security features to our services. All customers must get their accounts verified again.” (Van Der Heijden, A., & Allodi, L., 2019\) |
| Authority | “Tendency to obey people in authoritative positions, following from the possibility of punishment for not complying with the authoritative requests.” (Van Der Heijden, A., & Allodi, L., 2019\) | “Best regards, Executive Vice President of \<company name\>” (Van Der Heijden, A., & Allodi, L., 2019\) |
| Liking | “Preference for saying “yes” to the requests of people they know and like. People are programmed to like others who like them back and who are similar to them.” (Van Der Heijden, A., & Allodi, L., 2019\) | “We care for our customers and their online security. Confirm your identity .. so we can continue protecting you.” (Van Der Heijden, A., & Allodi, L., 2019\) |
| Scarcity | “Tendency to assign more value to items and opportunities when their availability is limited, not to waste the opportunity.” (Van Der Heijden, A., & Allodi, L., 2019\) | “If your account information is not updated within 48 hours then your ability to access your account will be restricted.” (Van Der Heijden, A., & Allodi, L., 2019\) |
| Commitment | “Refers to the likelihood of sticking to a cause or idea after making a promise or adhesion. In general, when a promise is made, people will honour it, which increases the likelihood of compliance.” (Bullée, J.-W., Montoya, L., Pieters, W., Junger, M., & Hartel, P, 2018\) | “As you agreed during our last vendor evaluation meeting, please proceed with the attached wire transfer request to finalize the contract.” |
| Urgency | “A technique that applies pressure on the victim to act quickly without giving him or her the time to consider their actions.” (Papathanasiou, A., Liontos, G., Liagkou, V., & Glavas, E. (2023) | “URGENT: This invoice is severely overdue. If payment is not initiated before the close of business today, the acquisition deal will fall through.” “Could you also please confirm the date when my next pay would come in? I need it to finish applying and just want to make sure the schedule hasn’t shifted due to the calendar.” (Response, M. D. E. C. I., 2026\) |

* **Tactics taxonomy.**  
  * The following table provides definitions and examples of the tactics used in campaigns.

| Tactic Name | Definition | Example |
| :---- | :---- | :---- |
| Display \- name spoofing | “This scheme uses the name of the spoofed executive in the ‘From’ Field. But the email address actually comes from an outside service such as Gmail that belongs to the attacker.” (Proofpoint, 2020\) | Real case. From: “Jane Smith” \<jane.smith@company.com\> Spoof case. From: “Jane Smith” \<j.smith8847@gmail.com\> |
| Domain spoofing | “This tactic involves an attacker hijacking your domain to send fraudulent emails to your employees, partners and customers. Attackers exploit the trust people place in your company brand name to steal money and valuable information.” (Proofpoint, 2020\) | Spoof case:  The fraudulent email is sent from the exact legitimate domain (e.g., From: “CEO” \<ceo@yourcompany.com\>) because the attacker exploits the lack of email authentication controls (like DMARC) on the victim’s domain. |
| Lookalike domains | In this scheme, “the attacker registers a domain that looks confusingly similar to a trusted legitimate domain.” (Proofpoint, 2020\) | Real case: ‘legitcompany.com’, Spoof case: ‘legtcompany.com’   |
| Reply-To manipulation | “Another tactic adopted by attackers is to use a faked organisation’s true domain in the ‘From’ address box. Adding another domain to the ‘Reply-To’ address box tricks the users into thinking they have received a reply. A reply to a field controlled by the attacker results in a reply being sent back to the attacker.” (Atlam, H. F., & Oluwatimilehin, O., 2023\) | Spoof case: From: billing@legit.com Reply-To: billing-legit@attacker.com |
| Message encoding / obfuscation | “To avoid being detected by email gateways, BEC attackers sometimes utilise encoding ploys that alter the characters in the message. When a BEC message is opened in the email account of a client, it seems to be a regular email. A hex editor scan, on the other hand, reveals the real colours of the image.” (Atlam, H. F., & Oluwatimilehin, O., 2023\) | Spoof case: Using zero-width spaces or homoglyphs in the email body so security filters read “I n v o i c e” while the human eye reads “Invoice”. |
| Adversary-in-the-middle (AiTM). | A technique where an attacker deploys a proxy server between a user and a legitimate service to intercept credentials and session cookies, bypassing multi-factor authentication (MFA). (Microsoft Threat Intelligence, 2023\) | Real case: The victim clicks a phishing link and logs into a fake Microsoft 365 page. The proxy captures their session cookie, allowing the attacker to bypass MFA and access the account. |
| Compromised legitimate account (ATO). | Account Takeover (ATO) occurs when an attacker gains unauthorized access to a legitimate employee’s email account and uses it to conduct fraudulent activities from within the organization. (FBI IC3, 2025\) | Real case: An attacker logs into the CFO’s actual email account using stolen credentials and sends an email to the finance department requesting a wire transfer. The email passes all authentication checks because it is genuine. |
| Mailbox rule manipulation. | The unauthorized creation or modification of email inbox rules by an attacker who has compromised an account, designed to conceal malicious communications from the victim. (Patterson, 2026\) | Real case: An attacker creates an Outlook rule that automatically moves any incoming email containing the words “fraud” or “bank” to the “RSS Feeds" or “Deleted Items” folder so the victim never sees security warnings. |
| Compromised third-party vendor account. | Also known as Vendor Email Compromise (VEC). An attacker compromises the email account of a trusted supplier and uses that established trust to request fraudulent payments from the vendor's customers. (Abnormal Security) | Real case: An attacker breaches a logistics supplier's email account and sends an email to all of their clients stating: “Our bank details have changed, please send all future payments to this new account.” |
| Malicious attachment | A tailored message carries a file (e.g., an Office document, executable, PDF, or archive) that delivers malware or gives the attacker access once the victim opens it. It differs from other forms of spearphishing in that it relies on malware attached to the message. (MITRE ATT\&CK, T1566.001)  | Illustrative case: A finance employee receives a message that appears to come from a known supplier with an attached archive; opening the file runs a loader on the employee’s device.  |
| Malicious link / redirect | A tailored message contains a link that sends the victim to an attacker-controlled resource (e.g., a file download or an intermediate page) in order to gain access to the victim’s systems, instead of carrying a file itself. (MITRE ATT\&CK, T1566.002)  | Illustrative case: An email posing as a business partner includes a link that redirects through an intermediate page to a download hosted on attacker infrastructure.  |
| Fake login / credential-collection page | A tailored message directs the victim to a web page that imitates a legitimate login or portal so that the credentials entered are captured by the attacker. Coding rule: when the report also describes session-cookie capture or MFA bypass, “Adversary-in-the-middle (AiTM)” is coded as well. (MITRE ATT\&CK, T1598.003) | Illustrative case: A link in an email posing as the organization’s IT department opens a page copying the company’s single sign-on screen; the submitted credentials go to the attacker.  |

* **Attack Classification: Value definitions**

| Value | Definition |
| :---- | :---- |
| Pure BEC (Impersonation \+ Fraud) | Targeted impersonation of a vendor/supplier or internal personnel whose objective is to obtain funds, or confidential information requested through the impersonation itself, by a direct request. No other attack vector is required beforehand. |
| Pure Spear Phishing (Targeted lure \+ Impersonation) | Targeted, tailored lure involving impersonation of a person, role, organization, or service that leads to credential disclosure, payload execution, data theft, or access. No other attack vector is required beforehand. Objectives that are BEC are classified as “*Pure BEC*” |
| Hybrid Campaign \- Targeting and impersonation necessary (other vector \- specify) | Another attack vector (e.g., AiTM, SEO poisoning / malvertising, compromised infrastructure) is necessary before or alongside the targeted impersonation to carry out the objective. This value takes precedence over the two Pure values. The additional vector(s) must be named in the row; the attacker's final objective is recorded in "*Request*" and "*Impact*". |
| Impersonation unnecessary (OUT OF SCOPE) | Impersonation is not part of the attack path. |
| No target selection (OUT OF SCOPE) | No evidence of the target selection (mass or opportunistic delivery). See “*Test for targeting*” |

	  
**Precedence:** In the event that stolen credentials are obtained at some stage of the attack and are subsequently used to carry out a fraudulent request (e.g., payroll diversion), the campaign is coded as “*Hybrid*” only if an additional vector was required to reach that stage; otherwise it is classified by its final objective.

**Campaign variables**

| Variable | Definition | Possibles results | Example |
| :---- | :---- | :---- | :---- |
| Campaign ID | Unique campaign identifier | Auto-generated, unique per row | CMP-0001 |
| Campaign Name | Name by which the campaign | Open response | Storm 2755 Payroll pirate attacks |
| Publisher | Auditor or Organization(s) publishing the public report. | Microsoft Threat Intelligence Proofpoint Abnormal Mandiant Cofense APWG FBI IC3 Other (specify) Not specified in the report Conflicting (see note) | Microsoft Threat Intelligence |
| Publisher Type | The type of institution publishing the report. | Government Vendor Academic Non-profit Other (specify) Not specified in the report Conflicting (see note) | Vendor |
| Publication Date | The date the campaign report was published | YYYY-MM-DD format Other (specify) Not specified in the report Conflicting (see note) | 2026-04-09 |
| Case Source Type | Specifies whether the campaign was obtained from a standalone campaign report or extracted as an illustrative case within an aggregate report. | Standalone campaign report Illustrative case within aggregate report Non-real life case (OUT OF SCOPE) | Standalone campaign report |
| Campaign Specificity | Specifies whether the entry represents a single, distinguishable spear phishing incident with an identifiable sequence of events, or an aggregated summary. | Single campaign Multi-Campaign aggregate / Generalized trend (OUT OF SCOPE) | Single campaign |
| Attack Classification | Specifies whether the campaign is a pure BEC campaign, a pure (non-BEC) spear phishing campaign, or a hybrid campaign that needs another attack vector, or whether it falls out of scope (see "Attack Classification: value definitions"). Evaluated first (Rule 1).  | Pure BEC (Impersonation \+ Fraud) Pure Spear Phishing (Targeted lure \+ Impersonation) Hybrid Campaign \- Targeting and impersonation necessary (other vector \- specify) Impersonation unnecessary (OUT OF SCOPE) No target selection (OUT OF SCOPE) | Hybrid Campaign \- Targeting and impersonation necessary (SEO poisoning / malvertising, AiTM) |
| Targeting Evidence | The explicit evidence in the report that the organization, sector segment, or role was deliberately selected. | Open response Not specified in the report Conflicting (see note) | The actor relied exclusively on geographic targeting of Canadian users, combined with socially engineering HR or finance staff members using consistent email subject lines across compromised users. |
| Outcome | Whether the attack succeeded in achieving its objective (funds, data, credentials, or access). | Successful (funds/ data/credentials/access obtained) Thwarted / Prevented  Partial Not specified in the report Conflicting (see note) | Successful (funds/data/credentials/access obtained) |
| Target | The specific demographic, industry or region the attacker is aiming at. | Open response | Canadian employees |
| Channels | The communication medium or technical vector used to execute the attack. | Open response | Search engine (SEO poisoning/malvertising) \> Corporate email \> HR SaaS platform (Workday) |
| Channel Transition | The route the attack takes is carried out through different mediums. | None (single channel throughout) Email \> Phone call Email \> Messaging app Different email thread/domain Multiple transitions Other (specify) Not specified in the report Conflicting (see note) | Multiple transitions  |
| Tactics | Specific technique (social-engineering or technical) used to execute the attack, independent of channel. | Display \- name spoofing Domain spoofing Typosquatting / lookalike domain Homoglyph domain spoofing Fake reply-chain / thread hijacking Reply-To header manipulation Message encoding / obfuscation Compromised legitimate account (ATO) Mailbox rule manipulation Adversary-in-the-middle (AiTM) Compromised third-party vendor account Malicious attachment Malicious link / redirect Fake login / credential-collection page Other (specify) Not specified in the report Conflicting (see note) | Adversary-in-the-middle (AiTM). Compromised legitimate account (ATO). Mailbox rule manipulation. Other (specify) \- SEO poisoning / malvertising  |
| Roles | The identities of the entities involved in the attack. | Open response, structured in three sub-fields: Attacker Impersonated Role Victim | Attacker: Storm-2755. Impersonated Role: Employee. Victim: HR or finance staff members. |
| Request | The final action the attacker wants the victim to perform. | Open response | Change direct deposit details to redirect a payroll check to an attacker-controlled bank account. |
| Pretext | The fabricated story or social engineering lure used by the attacker to manipulate the victim. | Open response | Setting up a new banking package and needing to update direct deposit instructions before the upcoming pay date. |
| Persuasion Principle(s) | The psychological or social engineering principle(s) that the attacker leverages within the pretext to manipulate the victim into compliance. | Reciprocity Consistency Social Proof Authority Liking Scarcity Commitment Urgency Other (specify) Not specified in the report | Urgency. |
| Timing | The specific moment or point in the victim’s business process/calendar at which the attack was executed. Refers to when the attack occurred. | Real estate closing Invoice payment cycle Holiday Payroll cycle Other (specify) Not specific Not specified in the report Conflicting (see note) | Payroll cycle. |
| Impact | The final consequence or damage caused by the attack. | Open response | Direct financial loss for affected individuals and organizations due to diverted salary payments. |
| Information Website | The URL or source of the threat intelligence report used for the analysis. | Web link | [https\://www\.microsoft.com/en-us/security/blog/2026/04/09/investigating-storm-2755-payroll-pirate-attacks-targeting-canadian-employees/](https://www.microsoft.com/en-us/security/blog/2026/04/09/investigating-storm-2755-payroll-pirate-attacks-targeting-canadian-employees/)   |
| Coding Date | The date and time at which this row was coded or entered into the dataset. | ISO 8601 \- Coordinated Universal Time “Zulu” (YYYY-MM-DDThh:mm:ssZ) | 2026-10-20T08:28:00Z |
| Coder | Specifies the provenance of this row's coding: whether it was produced by an unverified LLM-assisted first pass, verified by a human after LLM assistance, or independently coded by two analysts for inter-rater comparison. | Human coded LLM assisted Human verified Dual coded | Human coder |
| License | The usage license or terms of use declared by the source report’s publisher. | Public domain / government work Creative Commons (specify variant) All rights reserved (research / fair-use citation only) \- Specify Not specified in the source Other (specify) | All rights reserved (research / fair-use citation only) \- © Microsoft 2026 |
| Note on Ambiguity | Any situation where the report does not provide sufficient information, or presents contradictory information, preventing clear assignment of a value to the project’s core variables (channel, roles, requests, pretexts, timing). | Open response | None |
| Agreement Rate | Percent agreement for this row between two independent analysts: the number of compared variables with identical values divided by the number of variables compared. Cohen’s κ is computed per variable across the dual-coded sample and reported in the coding and agreement protocol, not stored in this row. **Default Rule:** Must be “N/A” unless “Coder” is “Dual coded”.  | 0% \- 100% N/A | N/A |

**Report variables**

| Variable | Definition | Possible results | Example |
| :---- | :---- | :---- | :---- |
| Report ID | Unique report identifier | Auto-generated, unique per row | REP-0011 |
| Report Name | Name by which by report is known | Open response | 2025 Internet Crime Report |
| Report Type | Type of report | Trimestral Landscape Annual Other (specify) Not specified in the report Conflicting (see note)  | Annual |
| Period Report | Period covered by the report | Annual Q1 Q2 Q3 Q4 Other (specify) Not specified in the report Conflicting (see note) | Annual |
| Report Year | Year of the report | YYYY format Other (specify) Not specified in the report Conflicting (see note) | 2025 |
| Geographic Scope | Geographic area covered by the report | Global  U.S. Other (specify) Not specified in the report Conflicting (see note) | Global |
| Publisher | Auditor or Organization(s) publishing the public report. | FBI IC3 Microsoft APWG Proofpoint Abnormal Mandiant Cofense Other (specify) Not specified in the report Conflicting (see note) | FBI IC3 |
| Publisher Type | The type of institution publishing the report. | Government Vendor Academic Non-profit Other (specify) Not specified in the report Conflicting (see note) | Government |
| Data Source | How the data was obtained. | Self-reported victims Vendor customer telemetry Other (specify) Not specified in the report Conflicting (see note) | Self-reported victims |
| Incident Counts | Number of incidents reported. | Other numeric response (integer) Not specified in the report Conflicting (see note) | 24,768 |
| Financial Loss | Amount of money reported as targeted-phishing (BEC / spear phishing)-related losses | Other numeric response (USD or other currency) Not specified in the report Conflicting (see note) | USD \$3,046,598,558  |
| Information Website | The URL or source of the threat intelligence report used for the analysis. | Web link | [https\://www\.ic3.gov/AnnualReport/Reports/2025\_IC3Report.pdf](https://www.ic3.gov/AnnualReport/Reports/2025_IC3Report.pdf)  |
| Coding Date | The date and time at which this row was coded or entered into the dataset. | ISO 8601 \- Coordinated Universal Time “Zulu” (YYYY-MM-DDThh:mm:ssZ) | 2026-10-11T20:47:00Z |
| Coder | Specifies the provenance of this row's coding: whether it was produced by an unverified LLM-assisted first pass, verified by a human after LLM assistance, or independently coded by two analysts for inter-rater comparison. | Human coded LLM assisted Human verified Dual coded | Human coder |
| License | The usage license or terms of use declared by the source report’s publisher. | Public domain / government work  Creative Commons (specify variant) All rights reserved (research / fair-use citation only) \- Specify Not specified in the source Other (specify) | Public domain / government work |
| Note on Ambiguity | Any situation where the aggregate report does not clearly indicate whether a figure corresponds exclusively to BEC or to broader OSP, does not specify how the data was obtained, or presents figures that overlap with other categories in the same report. | Open response | The report lists 24,768 complaints and \$3,046,598,558 in losses under 'Business Email Compromise'. Consistent with the methodology established since 2022, this category is understood to encompass both organizational (BEC) and personal email compromise (EAC). It remains impossible to isolate the figures corresponding exclusively to Organizational Spear Phishing. |
| Agreement Rate | Percent agreement for this row between two independent analysts: the number of compared variables with identical values divided by the number of variables compared. Cohen's κ is computed per variable across the dual-coded sample and reported in the coding and agreement protocol, not stored in this row. **Default Rule:** Must be “N/A” unless “Coder” is “Dual coded”.   | 0% \- 100% N/A | N/A |

**References**

1. Van Der Heijden, A., & Allodi, L. (2019). Cognitive triaging of phishing attacks. In 28th USENIX Security Symposium (USENIX Security 19\) (pp. 1309-1326).  [https\://www\.usenix.org/system/files/sec19-van\_der\_heijden.pdf](https://www.usenix.org/system/files/sec19-van_der_heijden.pdf)  
2. Tang, C. (2020, February 6). Three Common Business Email Compromise Tactics and How to Fight Back. Proofpoint. [https\://www\.proofpoint.com/us/corporate-blog/post/three-common-business-email-compromise-tactics-and-how-fight-back](https://www.proofpoint.com/us/corporate-blog/post/three-common-business-email-compromise-tactics-and-how-fight-back)  
3. Muscat, I. (2026, March 31). Display name spoofing. Have I Been Squatted. [https\://haveibeensquatted.com/learn/email-security/display-name-spoofing](https://haveibeensquatted.com/learn/email-security/display-name-spoofing)  
4. Atlam, H. F., & Oluwatimilehin, O. (2023). Business Email Compromise Phishing Detection Based on Machine Learning: A Systematic Literature Review. Electronics, 12(1), 42\. [https\://doi.org/10.3390/electronics12010042](https://doi.org/10.3390/electronics12010042)   
5. Microsoft Threat Intelligence. (2023, June 8). Detecting and mitigating a multi-stage AiTM phishing and BEC campaign. Microsoft Security Blog. [https\://www\.microsoft.com/en-us/security/blog/2023/06/08/detecting-and-mitigating-a-multi-stage-aitm-phishing-and-bec-campaign/](https://www.microsoft.com/en-us/security/blog/2023/06/08/detecting-and-mitigating-a-multi-stage-aitm-phishing-and-bec-campaign/)  
6. Federal Bureau of Investigation (FBI). (2025, November 25). Account Takeover Fraud via Impersonation of Financial Institution Support. Internet Crime Complaint Center (IC3). [https\://www\.ic3.gov/PSA/2025/PSA251125](https://www.ic3.gov/PSA/2025/PSA251125)  
7. Abnormal Security. (n.d.). CISO Guide to Vendor Email Compromise. [https\://files.abnormalsecurity.com/production/files/CISO-Guide-to-VEC.pdf](https://files.abnormalsecurity.com/production/files/CISO-Guide-to-VEC.pdf)  
8. Patterson, A. (2026, April 20). Inbox Rule Abuse: How Threat Actors Subvert Business Communication. Cynet Unified, AI-Powered Security Platform for MSPs & SMEs. [https\://www\.cynet.com/blog/inbox-rule-abuse-how-threat-actors-subvert-business-communication/](https://www.cynet.com/blog/inbox-rule-abuse-how-threat-actors-subvert-business-communication/)  
9. Bullée, J.-W., Montoya, L., Pieters, W., Junger, M., & Hartel, P. (2018). On the anatomy of social engineering attacks: A literature-based dissection of successful attacks. *Journal of Investigative Psychology and Offender Profiling*, *15*(1), 20-45. [https\://doi.org/10.1002/jip.1482](https://doi.org/10.1002/jip.1482)   
10. Papathanasiou, A., Liontos, G., Liagkou, V., & Glavas, E. (2023). Business Email Compromise (BEC) Attacks: Threats, Vulnerabilities and Countermeasures—A Perspective on the Greek Landscape. Journal of Cybersecurity and Privacy, 3(3), 610-637. [https\://doi.org/10.3390/jcp3030029](https://doi.org/10.3390/jcp3030029)  
11. Response, M. D. E. C. I. (2026, April 9). Investigating Storm-2755: “Payroll pirate” attacks targeting Canadian employees. Microsoft Security Blog. [https\://www\.microsoft.com/en-us/security/blog/2026/04/09/investigating-storm-2755-payroll-pirate-attacks-targeting-canadian-employees/](https://www.microsoft.com/en-us/security/blog/2026/04/09/investigating-storm-2755-payroll-pirate-attacks-targeting-canadian-employees/)  
12. Phishing: Spearphishing Attachment, Sub-technique T1566.001 \- Enterprise \| MITRE ATT\&CK®. (n.d.). MITRE \| ATT\&CK. [https\://attack.mitre.org/techniques/T1566/001/](https://attack.mitre.org/techniques/T1566/001/)  
13. Phishing: Spearphishing Link, Sub-technique T1566.002 \- Enterprise \| MITRE ATT\&CK®. (n.d.). MITRE \| ATT\&CK. [https\://attack.mitre.org/techniques/T1566/002/](https://attack.mitre.org/techniques/T1566/002/)  
14. Phishing for Information: Spearphishing Link, Sub-technique T1598.003 \- Enterprise \| MITRE ATT\&CK®. (n.d.). MITRE \| ATT\&CK. [https\://attack.mitre.org/techniques/T1598/003/](https://attack.mitre.org/techniques/T1598/003/) 