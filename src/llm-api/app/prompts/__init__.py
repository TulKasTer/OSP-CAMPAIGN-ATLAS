"""System and user prompt templates grounded in FREEZE CODING SCHEME V2.1, DATASET SCHEMA V2.1, and CODING ORDER V1.0."""

from .campaign_prompts import (
    CAMPAIGN_GATES_SYSTEM_PROMPT,
    CAMPAIGN_FULL_CODING_SYSTEM_PROMPT,
    build_campaign_gates_user_prompt,
    build_campaign_full_coding_user_prompt,
)
from .report_prompts import (
    REPORT_CODING_SYSTEM_PROMPT,
    build_report_coding_user_prompt,
)

__all__ = [
    "CAMPAIGN_GATES_SYSTEM_PROMPT",
    "CAMPAIGN_FULL_CODING_SYSTEM_PROMPT",
    "build_campaign_gates_user_prompt",
    "build_campaign_full_coding_user_prompt",
    "REPORT_CODING_SYSTEM_PROMPT",
    "build_report_coding_user_prompt",
]
