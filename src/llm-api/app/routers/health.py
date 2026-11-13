"""Health check and schema inspection endpoints."""

from __future__ import annotations

import json
from typing import Any
from fastapi import APIRouter

from ..config import (
    CAMPAIGN_SCHEMA_FILE,
    EXCLUSION_LOG_SCHEMA_FILE,
    METADATA_SCHEMA_FILE,
    REPORT_SCHEMA_FILE,
    get_settings,
)
from ..schemas.common import (
    ATTACK_CLASSIFICATION_VALUES,
    CAMPAIGN_PUBLISHERS,
    CAMPAIGN_SPECIFICITY_VALUES,
    CASE_SOURCE_TYPE_VALUES,
    CHANNEL_TRANSITION_VALUES,
    DATA_SOURCE_VALUES,
    GEOGRAPHIC_SCOPE_VALUES,
    OUTCOME_VALUES,
    PERIOD_REPORT_VALUES,
    PERSUASION_PRINCIPLES_TAXONOMY,
    PUBLISHER_TO_TYPE_MAP,
    REPORT_TYPE_VALUES,
    TACTICS_TAXONOMY,
    TIMING_VALUES,
)

router = APIRouter(tags=["System & Schemas"])


def _read_json_safe(path) -> dict[str, Any]:
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
    return {}


@router.get("/health", summary="Check API health, LLM sampling, and RAM/VRAM configuration")
def health_check() -> dict[str, Any]:
    """Return service status, active LLM model configuration, hardware limits, and schema references."""
    settings = get_settings()
    return {
        "status": "ok",
        "service": "osp-campaign-atlas-llm-api",
        "version": "1.0.0",
        "llm_config": {
            "model": settings.model,
            "api_base": settings.api_base,
            "local_api_base": settings.local_api_base,
            "max_retries": settings.max_retries,
            "timeout_seconds": settings.timeout_seconds,
            "api_key_configured": bool(settings.api_key),
        },
        "sampling_config": {
            "temperature": settings.temperature,
            "gates_temperature": settings.gates_temperature,
            "coding_temperature": settings.coding_temperature,
            "top_p": settings.top_p,
            "top_k": settings.top_k,
            "min_p": settings.min_p,
            "repeat_penalty": settings.repeat_penalty,
            "presence_penalty": settings.presence_penalty,
            "frequency_penalty": settings.frequency_penalty,
            "max_tokens": settings.max_tokens,
            "seed": settings.seed,
        },
        "hardware_memory_config": {
            "num_ctx": settings.num_ctx,
            "num_gpu": settings.num_gpu,
            "main_gpu": settings.main_gpu,
            "num_thread": settings.num_thread,
            "num_batch": settings.num_batch,
            "use_mmap": settings.use_mmap,
            "use_mlock": settings.use_mlock,
            "low_vram": settings.low_vram,
            "keep_alive": settings.keep_alive,
        },
        "references": {
            "freeze_coding_schema": "FREEZE CODING SCHEME V2.1 (2026-10-26)",
            "dataset_schema": "DATASET SCHEMA V2.1 (2026-10-26)",
            "coding_order": "CODING ORDER V1.0 (2026-10-30)",
            "schema_docs": "SCHEMA DOCS V1.0 (2026-10-30)",
        },
    }


@router.get("/api/v1/schemas", summary="Get canonical JSON schemas and frozen taxonomies")
def get_schemas_and_taxonomies() -> dict[str, Any]:
    """Return canonical JSON templates from `schemas/` and frozen taxonomies from DATASET SCHEMA V2.1."""
    return {
        "json_templates": {
            "campaign": _read_json_safe(CAMPAIGN_SCHEMA_FILE),
            "report": _read_json_safe(REPORT_SCHEMA_FILE),
            "exclusion_log": _read_json_safe(EXCLUSION_LOG_SCHEMA_FILE),
            "metadata": _read_json_safe(METADATA_SCHEMA_FILE),
        },
        "taxonomies": {
            "attack_classification": list(ATTACK_CLASSIFICATION_VALUES),
            "case_source_type": list(CASE_SOURCE_TYPE_VALUES),
            "campaign_specificity": list(CAMPAIGN_SPECIFICITY_VALUES),
            "tactics": list(TACTICS_TAXONOMY),
            "persuasion_principles": list(PERSUASION_PRINCIPLES_TAXONOMY),
            "channel_transition": list(CHANNEL_TRANSITION_VALUES),
            "outcome": list(OUTCOME_VALUES),
            "timing": list(TIMING_VALUES),
            "publishers": list(CAMPAIGN_PUBLISHERS),
            "publisher_to_type_map": PUBLISHER_TO_TYPE_MAP,
            "report_type": list(REPORT_TYPE_VALUES),
            "period_report": list(PERIOD_REPORT_VALUES),
            "geographic_scope": list(GEOGRAPHIC_SCOPE_VALUES),
            "data_source": list(DATA_SOURCE_VALUES),
        },
    }
