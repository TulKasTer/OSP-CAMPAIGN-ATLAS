"""Endpoints for fetching URL source metadata and SHA-256 hashes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..schemas.api import SourceMetadataRequest, SourceMetadataResponse
from ..services.scraper import fetch_url_content_and_metadata
from ..services.storage import AtlasStorageService

router = APIRouter(prefix="/api/v1/sources", tags=["Source Metadata"])


@router.post(
    "/metadata",
    response_model=SourceMetadataResponse,
    summary="Fetch URL metadata, SHA-256 hash, and optional extracted text",
)
def extract_source_metadata(request: SourceMetadataRequest) -> SourceMetadataResponse:
    """Download a report URL, compute its SHA-256 hash, extract OpenGraph/HTML metadata
    matching `schemas/metadata-schema.json`, and optionally persist to `data/raw/`.
    """
    try:
        fetched = fetch_url_content_and_metadata(request.url)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to fetch URL '{request.url}': {exc}") from exc

    saved_paths: list[str] = []
    if request.save_to_disk:
        saved_paths = AtlasStorageService.save_source_metadata(
            metadata=fetched.metadata,
            target_type=request.target_type,
            folder_slug=request.folder_slug,
        )

    return SourceMetadataResponse(
        metadata=fetched.metadata,
        extracted_text=fetched.extracted_text if request.include_extracted_text else None,
        saved_paths=saved_paths,
    )
