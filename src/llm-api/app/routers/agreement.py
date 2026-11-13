"""Endpoints for Inter-Rater Agreement (Row % Agreement & Cohen's kappa) and Schema Validation."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas.api import (
    DatasetAgreementRequest,
    DatasetAgreementResponse,
    RowAgreementRequest,
    RowAgreementResponse,
    ValidateRecordRequest,
    ValidateRecordResponse,
)
from ..services.agreement import (
    compute_dataset_agreement,
    compute_row_agreement,
    validate_atlas_record,
)

router = APIRouter(prefix="/api/v1", tags=["Agreement & Validation"])


@router.post(
    "/agreement/row",
    response_model=RowAgreementResponse,
    summary="Compute row-level percentage agreement (0%-100%) between two independent codings",
)
def calculate_row_agreement(request: RowAgreementRequest) -> RowAgreementResponse:
    """Compute row-level `agreement_rate` between two independent analysts (Human/Human or LLM/Human)
    as defined in DATASET SCHEMA V2.1 and Registered Protocol V1.
    """
    try:
        return compute_row_agreement(request)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    "/agreement/dataset",
    response_model=DatasetAgreementResponse,
    summary="Compute Cohen's kappa (κ) and % agreement across a dual-coded sample",
)
def calculate_dataset_agreement(request: DatasetAgreementRequest) -> DatasetAgreementResponse:
    """Compute dataset-level Cohen's kappa (κ) and percentage agreement across dual-coded campaigns
    for `attack_classification`, `targeting_evidence`, `Hybrid other vector`, `persuasion_principles` (per label),
    and `tactics` (per label) per Registered Protocol V1.
    """
    try:
        return compute_dataset_agreement(request)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post(
    "/validate",
    response_model=ValidateRecordResponse,
    summary="Validate and normalize a Campaign, Report, or Exclusion Log JSON record",
)
def validate_record(request: ValidateRecordRequest) -> ValidateRecordResponse:
    """Validate a JSON payload against FREEZE CODING SCHEME V2.1 and DATASET SCHEMA V2.1 rules."""
    return validate_atlas_record(request)
