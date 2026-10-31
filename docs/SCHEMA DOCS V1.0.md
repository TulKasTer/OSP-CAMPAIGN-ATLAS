# SCHEMA DOCS V1.0
**Version:** 1.0  
**Date:** 2026-10-30  
**Coding schema reference:** FREEZE CODING SCHEMA V2.1 (2026-10-26).\
**Dataset schema reference:** DATASET SCHEMA V2.1 (2026-10-26).

El proyecto tiene schemas bases para la codificacion de las tablas de `Campaign` & `Report`, los cuales se encuentran ubicados en la carpeta de `schemas/`, esta tiene el siguiente organización:

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

## Campaigns schemas

Los schemas de campañas sirven para codificar las campañas extraidas de los informes recopilados en formato JSON, con el objetivo de poder utilizar despues dicha codificacion para el Atlas en la tabla de `Campaign`, para esto existen los siguientes schemas:

- Campaign human coded schema
- Campaign schema
- Campaign sources dataset schema
- Campaigns dataset schema
- Exclusion log schema

### Campaign human coded schema
El `Campaign human coded schema` es un esquema de codificacion que permite que los codificadores humanos llenar la fila de codificacion de una campaña extraido de un informe.

- [ ] Obligatorio de usar
- [x] El codificador humano puede usarlo
- [x] Es un schema que puede desaparecer en un futuro.
- [x] Es sustituible.

Se usa en la fase de codificacion manual por un investigación humano.

Ubicacion en el proyecto: `schemas\campaigns\campaign-human-coded-schema.json`

Estructura del schema:
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
> Este schema se creo para agilizar el proceso de codificación manual del primer dataset, este puede sustituir al ´campaign-schema.json´ en casos de codificacion por humanos y en un futuro puede desaparecer una vez se determine la architectura definitiva del proyecto.

### Campaign schema
El `Campaign schema` es un esquema de codificacion que permite que los codificadores humanos y/o LMMs llenar la fila de codificacion de una campaña extraido de un informe.

- [x] Obligatorio de usar
- [x] El codificador humano puede usarlo
- [ ] Es un schema que puede desaparecer en un futuro.
- [x] Es sustituible.

Se usa en la fase de codificacion manual por un investigación humano y por parte de LLMs.

Ubicacion en el proyecto: `schemas\campaigns\campaign-schema.json`

Estructura del schema:
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
El `Campaign sources dataset schema` es un esquema de codificacion que permite que los codificadores humanos y/o LMMs declaron los metadatos de las paginas web donde se encuentran los informes.

- [x] Obligatorio de usar
- [x] El codificador humano puede usarlo
- [ ] Es un schema que puede desaparecer en un futuro.
- [ ] Es sustituible.

Se usa en la fase de codificacion manual por un investigación humano y por parte de LLMs.

Ubicacion en el proyecto: `schemas\campaigns\campaign-sources-dataset-schema.json`

Estructura del schema:
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
> Este schema se creo para declara los metadatos de las fuentes de donde se obtuvieron los reportes, en caso de ya ver sido codificada por el coder principal, los proximos codificadores no deben de codificar esos datos.

### Campaigns dataset schema
El `Campaigns dataset schema` es un esquema de codificacion que permite que los codificadores humanos y/o LMMs, juntar las codificaciones individuales de cada campaña en un solo archivo, de manera que pueda crearse un dataset.

- [x] Obligatorio de usar
- [x] El codificador humano puede usarlo
- [ ] Es un schema que puede desaparecer en un futuro.
- [ ] Es sustituible.

Se usa en la fase de codificacion manual por un investigación humano y por parte de LLMs.

Ubicacion en el proyecto: `schemas\campaigns\campaigns-dataset-schema.json`

Estructura del schema:
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
El `Exclusion log schema` es un esquema de codificacion que permite que los codificadores humanos y/o LMMs, aqui se codifican aquellas campañas o informes que fueron excluidos con el motivo de su exclusión.

- [x] Obligatorio de usar
- [x] El codificador humano puede usarlo
- [ ] Es un schema que puede desaparecer en un futuro.
- [ ] Es sustituible.

Se usa en la fase de codificacion manual por un investigación humano y por parte de LLMs.

Ubicacion en el proyecto: `schemas\campaigns\exclusion-log-schema.json`

Estructura del schema:
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

## Reports schemas

Los schemas de reportes sirven para codificar las datos de los reportes extraidos de los informes recopilados en formato JSON, con el objetivo de poder utilizar despues dicha codificacion para el Atlas en la tabla de `Report`, para esto existen los siguientes schemas:

- Report human coded schema
- Report schema
- Report source dataset schema
- Report dataset schema

### Report human coded shema
El `Report human coded schema` es un esquema de codificacion que permite que los codificadores humanos llenar la fila de codificacion de una campaña extraido de un informe.

- [ ] Obligatorio de usar
- [x] El codificador humano puede usarlo
- [x] Es un schema que puede desaparecer en un futuro.
- [x] Es sustituible.



Ubicacion en el proyecto: `schemas\reports\report-human-coded-schema.json`

Estructura del schema:
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
> Este schema se creo para agilizar el proceso de codificación manual del primer dataset. No sustituye al `report-schema.json`; es una plantilla con valores predeterminados para la codificación humana.

### Report schema
El `Report schema` es el esquema general para codificar los datos de un reporte. Puede ser utilizado por codificadores humanos y/o LMMs.

- [x] Obligatorio de usar
- [x] El codificador humano puede usarlo
- [ ] Es un schema que puede desaparecer en un futuro.
- [ ] Es sustituible.

Se usa en la fase de codificación manual por un investigador humano y por parte de LLMs.

Ubicacion en el proyecto: `schemas\reports\report-schema.json`

Estructura del schema:
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
El `Report source dataset schema` permite registrar los metadatos de las fuentes utilizadas para los reportes.

- [x] Obligatorio de usar
- [x] El codificador humano puede usarlo
- [ ] Es un schema que puede desaparecer en un futuro.
- [ ] Es sustituible.

Ubicacion en el proyecto: `schemas\reports\report-sources-dataset-schema.json`

Estructura del schema:
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
El `Report dataset schema` permite reunir las codificaciones individuales de los reportes en un solo archivo para crear el dataset.

- [x] Obligatorio de usar
- [x] El codificador humano puede usarlo
- [ ] Es un schema que puede desaparecer en un futuro.
- [ ] Es sustituible.

Ubicacion en el proyecto: `schemas\reports\reports-dataset-schema.json`

Estructura del schema:
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

## Extra schemas
El repositorio tiene schemas extra los cuales estan hecho para proporcionar algun model de partes no cubiertas por los schemas anteriormente mencionados. En este apartado existen:

- Metadata schema

### Metadata schema
El `Metadata schema` permite registrar los metadatos de una fuente individual. Sus campos son reutilizados por los schemas de fuentes de campañas y reportes.

Ubicacion en el proyecto: `schemas\metadata-schema.json`

Estructura del schema:
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
