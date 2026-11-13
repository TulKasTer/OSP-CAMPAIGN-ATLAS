"""Configuration and path settings for the OSP Campaign Atlas LLM API."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv

# Resolve repository root directory (OSP-CAMPAIGN-ATLAS/)
ROOT_DIR = Path(__file__).resolve().parents[3]

# Load environment variables from .env if present
load_dotenv(ROOT_DIR / ".env")

# Schema paths
SCHEMAS_DIR = ROOT_DIR / "schemas"
METADATA_SCHEMA_FILE = SCHEMAS_DIR / "metadata-schema.json"

CAMPAIGNS_SCHEMAS_DIR = SCHEMAS_DIR / "campaigns"
CAMPAIGN_SCHEMA_FILE = CAMPAIGNS_SCHEMAS_DIR / "campaign-schema.json"
CAMPAIGN_HUMAN_CODED_SCHEMA_FILE = CAMPAIGNS_SCHEMAS_DIR / "campaign-human-coded-schema.json"
CAMPAIGN_SOURCES_SCHEMA_FILE = CAMPAIGNS_SCHEMAS_DIR / "campaign-sources-dataset-schema.json"
CAMPAIGNS_DATASET_SCHEMA_FILE = CAMPAIGNS_SCHEMAS_DIR / "campaigns-dataset-schema.json"
EXCLUSION_LOG_SCHEMA_FILE = CAMPAIGNS_SCHEMAS_DIR / "exclusion-log-schema.json"

REPORTS_SCHEMAS_DIR = SCHEMAS_DIR / "reports"
REPORT_SCHEMA_FILE = REPORTS_SCHEMAS_DIR / "report-schema.json"
REPORT_HUMAN_CODED_SCHEMA_FILE = REPORTS_SCHEMAS_DIR / "report-human-coded-schema.json"
REPORT_SOURCES_SCHEMA_FILE = REPORTS_SCHEMAS_DIR / "report-sources-dataset-schema.json"
REPORTS_DATASET_SCHEMA_FILE = REPORTS_SCHEMAS_DIR / "reports-dataset-schema.json"

# Data paths
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
RAW_CAMPAIGNS_DIR = RAW_DATA_DIR / "campaigns"
RAW_REPORTS_DIR = RAW_DATA_DIR / "reports"

INTERIM_DATA_DIR = DATA_DIR / "interim"
INTERIM_HUMAN_CODED_DIR = INTERIM_DATA_DIR / "human-coded"
INTERIM_LLM_CODED_DIR = INTERIM_DATA_DIR / "llm-coded"
INTERIM_LLM_CAMPAIGNS_DIR = INTERIM_LLM_CODED_DIR / "campaigns"
INTERIM_LLM_REPORTS_DIR = INTERIM_LLM_CODED_DIR / "reports"

PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOG_DIR = ROOT_DIR / "logs"
EXCLUSION_LOG_FILE = LOG_DIR / "exclusion-log.log"

# Docs paths
DOCS_DIR = ROOT_DIR / "docs"


def _env_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return float(raw.strip())


def _env_optional_float(name: str) -> float | None:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return None
    return float(raw.strip())


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return int(raw.strip())


def _env_optional_int(name: str) -> int | None:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return None
    return int(raw.strip())


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class LLMSettings:
    """Runtime settings for LiteLLM + Instructor, sampling parameters, and local RAM/VRAM allocation."""

    # Server & Provider
    host: str = field(default_factory=lambda: os.getenv("LLM_API_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: _env_int("LLM_API_PORT", 5000))
    model: str = field(default_factory=lambda: os.getenv("LLM_MODEL") or "ollama/qwen3.5:9b")
    api_key: str | None = field(default_factory=lambda: os.getenv("LLM_API_KEY") or None)
    api_base: str | None = field(default_factory=lambda: os.getenv("LLM_API_BASE") or None)
    local_api_base: str = field(
        default_factory=lambda: os.getenv("LLM_LOCAL_API_BASE", "http://localhost:11434")
    )
    max_retries: int = field(default_factory=lambda: _env_int("LLM_MAX_RETRIES", 3))
    timeout_seconds: int = field(default_factory=lambda: _env_int("LLM_TIMEOUT_SECONDS", 180))
    default_evaluator: str = field(default_factory=lambda: os.getenv("LLM_EVALUATOR", "LLM-API"))

    # Temperatures & Sampling Parameters
    temperature: float = field(default_factory=lambda: _env_float("LLM_TEMPERATURE", 0.0))
    gates_temperature: float | None = field(
        default_factory=lambda: _env_optional_float("LLM_GATES_TEMPERATURE")
    )
    coding_temperature: float | None = field(
        default_factory=lambda: _env_optional_float("LLM_CODING_TEMPERATURE")
    )
    top_p: float | None = field(default_factory=lambda: _env_optional_float("LLM_TOP_P"))
    top_k: int | None = field(default_factory=lambda: _env_optional_int("LLM_TOP_K"))
    min_p: float | None = field(default_factory=lambda: _env_optional_float("LLM_MIN_P"))
    repeat_penalty: float | None = field(
        default_factory=lambda: _env_optional_float("LLM_REPEAT_PENALTY")
    )
    presence_penalty: float | None = field(
        default_factory=lambda: _env_optional_float("LLM_PRESENCE_PENALTY")
    )
    frequency_penalty: float | None = field(
        default_factory=lambda: _env_optional_float("LLM_FREQUENCY_PENALTY")
    )
    max_tokens: int | None = field(default_factory=lambda: _env_optional_int("LLM_MAX_TOKENS"))
    seed: int | None = field(default_factory=lambda: _env_optional_int("LLM_SEED"))

    # Local Model RAM / VRAM / Hardware Controls (Ollama / local runners)
    num_ctx: int = field(default_factory=lambda: _env_int("LLM_NUM_CTX", 16384))
    num_gpu: int = field(default_factory=lambda: _env_int("LLM_NUM_GPU", -1))
    main_gpu: int = field(default_factory=lambda: _env_int("LLM_MAIN_GPU", 0))
    num_thread: int = field(default_factory=lambda: _env_int("LLM_NUM_THREAD", 0))
    num_batch: int = field(default_factory=lambda: _env_int("LLM_NUM_BATCH", 512))
    use_mmap: bool = field(default_factory=lambda: _env_bool("LLM_USE_MMAP", True))
    use_mlock: bool = field(default_factory=lambda: _env_bool("LLM_USE_MLOCK", False))
    low_vram: bool = field(default_factory=lambda: _env_bool("LLM_LOW_VRAM", False))
    keep_alive: str = field(default_factory=lambda: os.getenv("LLM_KEEP_ALIVE", "10m"))


def get_settings() -> LLMSettings:
    """Return current LLM configuration from environment."""
    return LLMSettings()
