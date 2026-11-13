"""Endpoints for 2-phase Campaign coding and Gate #1-#3 eligibility evaluation."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas.api import (
    CodeCampaignRequest,
    CodeCampaignResponse,
    EvaluateGatesRequest,
    EvaluateGatesResponse,
)
from ..services.coder import AtlasCodingService

router = APIRouter(prefix="/api/v1/campaigns", tags=["Campaign Coding"])


@router.post(
    "/evaluate-gates",
    response_model=EvaluateGatesResponse,
    summary="Stage 1: Evaluate Campaign Eligibility Filters (Gates #1-#3)",
)
def evaluate_campaign_gates(request: EvaluateGatesRequest) -> EvaluateGatesResponse:
    """Evaluate Gate #1 (Attack Classification), Gate #2 (Case Source Type), and Gate #3 (Campaign Specificity)
    plus Target Identification (Phase 2). Generates an ExclusionLogRecord if any gate triggers an exclusion.
    """
    service = AtlasCodingService()
    try:
        return service.evaluate_campaign_gates(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Gate evaluation failed: {exc}") from exc


@router.post(
    "/code",
    response_model=CodeCampaignResponse,
    summary="2-Phase Campaign Coding (Gates #1-#3 -> 28 Variables)",
)
def code_campaign(request: CodeCampaignRequest) -> CodeCampaignResponse:
    """Run the 2-phase Campaign coding workflow per CODING ORDER V1.0 and FREEZE CODING SCHEME V2.1:
    1. Evaluates Gates #1-#3 (stops and returns ExclusionLogRecord if excluded, unless `force_full_coding=True`).
    2. Extracts all 28 variables across Phases 2-8 into the canonical `campaign-schema.json` structure.
    """
    service = AtlasCodingService()
    try:
        return service.code_campaign(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Campaign coding failed: {exc}") from exc
