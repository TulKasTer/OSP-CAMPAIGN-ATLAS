"""Endpoints for Aggregate Report coding (17 variables across 4 logical phases)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas.api import CodeReportRequest, CodeReportResponse
from ..services.coder import AtlasCodingService

router = APIRouter(prefix="/api/v1/reports", tags=["Aggregate Report Coding"])


@router.post(
    "/code",
    response_model=CodeReportResponse,
    summary="Code an Aggregate OSP/BEC Report (17 Variables)",
)
def code_report(request: CodeReportRequest) -> CodeReportResponse:
    """Extract all 17 variables for an aggregated threat intelligence report following
    the 4 sequential phases of CODING ORDER V1.0 and DATASET SCHEMA V2.1.
    """
    service = AtlasCodingService()
    try:
        return service.code_report(request)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Report coding failed: {exc}") from exc
