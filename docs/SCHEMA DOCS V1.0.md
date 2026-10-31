# SCHEMA DOCS V1.0
**Version:** 1.0  
**Date:** 2026-10-30  
**Coding schema reference:** FREEZE CODING SCHEMA V2.1 (2026-10-26).\
**Dataset schema reference:** DATASET SCHEMA V2.1 (2026-10-26).

The project has base schemas for coding the `Campaign` and `Report` tables. They are located in the `schemas/` folder, which has the following organization:

```
schemas/
├── metadata-schema.json
├── campaigns/
│   ├── campaign-human-coded-schema.json
│   ├── campaign-schema.json
│   ├── campaign-sources-dataset-schema.json
│   ├── campaigns-dataset-schema.json
│   └── exclusion-log-schema.json
└── reports/
    ├── report-human-coded-schema.json
    ├── report-schema.json
    ├── report-sources-dataset-schema.json
    └── reports-dataset-schema.json
```

## Campaign schemas

The campaign schemas are used to code campaigns extracted from collected reports in JSON format. The resulting coding can then be used in the Atlas `Campaign` table. The following schemas are available:

- Campaign human coded schema
- Campaign schema
- Campaign sources dataset schema
- Campaigns dataset schema
- Exclusion log schema

### Campaign human coded schema
The `Campaign human coded schema` is a coding schema that allows human coders to complete the coding row for a campaign extracted from a report.

- [ ] Required
- [x] Can be used by a human coder
- [x] May be removed in the future
- [x] Replaceable

It is used during the manual coding phase by a human researcher.

Project location: `schemas\campaigns\campaign-human-coded-schema.json`

Schema structure:
```
{
    "campaign_id": "REP-0000",
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
    "coder": "Human coded",
    "license": "",
    "note_on_ambiguity": "",
    "agreement_rate": "N/A"
    
}
```

> [!NOTE]
> This schema was created to streamline the manual coding process for the first dataset. It can replace `campaign-schema.json` when coding is performed by humans and may be removed in the future once the project's final architecture is determined.

### Campaign schema
The `Campaign schema` is a coding schema that allows human coders and/or LMMs to complete the coding row for a campaign extracted from a report.

- [x] Required
- [x] Can be used by a human coder
- [ ] May be removed in the future
- [x] Replaceable

It is used during the manual coding phase by a human researcher and by LLMs.

Project location: `schemas\campaigns\campaign-schema.json`

Schema structure:
```
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

### Campaign sources dataset schema
The `Campaign sources dataset schema` is a coding schema that allows human coders and/or LMMs to record the metadata of the web pages where the reports are located.

- [x] Required
- [x] Can be used by a human coder
- [ ] May be removed in the future
- [ ] Replaceable

It is used during the manual coding phase by a human researcher and by LLMs.

Project location: `schemas\campaigns\campaign-sources-dataset-schema.json`

Schema structure:
```
{
    "campaign_sources": [
        {
            "url": "",
            "title": "",
            "publisher": "",
            "author": "",
            "published_date": "",
            "retrieved_at_utc": "",
            "sha256_hash": ""
        }
    ]
} 
```

> [!NOTE]
> This schema was created to record the metadata of the sources from which the reports were obtained. If these data have already been coded by the primary coder, subsequent coders should not code them again.

### Campaigns dataset schema
The `Campaigns dataset schema` is a coding schema that allows human coders and/or LMMs to combine the individual codings for each campaign into a single file, creating a dataset.

- [x] Required
- [x] Can be used by a human coder
- [ ] May be removed in the future
- [ ] Replaceable

It is used during the manual coding phase by a human researcher and by LLMs.

Project location: `schemas\campaigns\campaigns-dataset-schema.json`

Schema structure:
```
{
    "campaigns": [
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
            "tactics": [
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
    ]
}
```

### Exclusion log schema
The `Exclusion log schema` is a coding schema that allows human coders and/or LMMs to record campaigns or reports that were excluded, together with the reason for their exclusion.

- [x] Required
- [x] Can be used by a human coder
- [ ] May be removed in the future
- [ ] Replaceable

It is used during the manual coding phase by a human researcher and by LLMs.

Project location: `schemas\campaigns\exclusion-log-schema.json`

Schema structure:
```
{
    "exclusion_log": [
        {
            "excluded_id": "",
            "campaign_name": "",
            "publisher": "",
            "information_website": "",
            "rule_triggered": "",
            "exclusion_reason": "",
            "exclusion_date": "",
            "evaluator": ""
        }
    ]
}
```

## Report schemas

The report schemas are used to code report data extracted from collected reports in JSON format. The resulting coding can then be used in the Atlas `Report` table. The following schemas are available:

- Report human coded schema
- Report schema
- Report source dataset schema
- Report dataset schema

### Report human coded schema
The `Report human coded schema` is a coding schema that allows human coders to complete the coding row for a report extracted from a source.

- [ ] Required
- [x] Can be used by a human coder
- [x] May be removed in the future
- [x] Replaceable

Project location: `schemas\reports\report-human-coded-schema.json`

Schema structure:
```
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
    "coder": "human coded",
    "license": "",
    "note_on_ambiguity": "",
    "agreement_rate": "N/A"
}
```
> [!NOTE]
> This schema was created to streamline the manual coding process for the first dataset. It does not replace `report-schema.json`; it is a template with default values for human coding.

### Report schema
The `Report schema` is the general schema for coding report data. It can be used by human coders and/or LMMs.

- [x] Required
- [x] Can be used by a human coder
- [ ] May be removed in the future
- [ ] Replaceable

It is used during the manual coding phase by a human researcher and by LLMs.

Project location: `schemas\reports\report-schema.json`

Schema structure:
```
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

### Report source dataset schema
The `Report source dataset schema` is used to record the metadata of the sources used for the reports.

- [x] Required
- [x] Can be used by a human coder
- [ ] May be removed in the future
- [ ] Replaceable

Project location: `schemas\reports\report-sources-dataset-schema.json`

Schema structure:
```
{
    "report_sources": [
        {
            "url": "",
            "title": "",
            "publisher": "",
            "author": "",
            "published_date": "",
            "retrieved_at_utc": "",
            "sha256_hash": ""
        }
    ]
}
```

### Report dataset schema
The `Report dataset schema` allows the individual codings for reports to be combined into a single file to create the dataset.

- [x] Required
- [x] Can be used by a human coder
- [ ] May be removed in the future
- [ ] Replaceable

Project location: `schemas\reports\reports-dataset-schema.json`

Schema structure:
```
{
    "reports": [
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
    ]
}
```

## Additional schemas
The repository includes additional schemas that provide models for parts not covered by the schemas described above. This section contains:

- Metadata schema

### Metadata schema
The `Metadata schema` allows the metadata of an individual source to be recorded. Its fields are reused by the campaign and report source schemas.

Project location: `schemas\metadata-schema.json`

Schema structure:
```
{
    "url": "",
    "title": "",
    "publisher": "",
    "author": "",
    "published_date": "",
    "retrieved_at_utc": "",
    "sha256_hash": ""
}
```
