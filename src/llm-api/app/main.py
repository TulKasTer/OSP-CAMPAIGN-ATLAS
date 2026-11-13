"""FastAPI application entrypoint for OSP Campaign Atlas LLM API."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .routers import (
    agreement_router,
    campaigns_router,
    health_router,
    reports_router,
    sources_router,
)


def create_app() -> FastAPI:
    """Create and configure the OSP Campaign Atlas LLM FastAPI application."""
    application = FastAPI(
        title="OSP Campaign Atlas — LLM Coding API",
        description=(
            "Structured LLM-assisted coding, eligibility gate evaluation (Rules #1-#3), "
            "source metadata extraction, and inter-rater reliability (Agreement Rate & Cohen's κ) "
            "for the Organizational Spear Phishing (OSP) Campaign Atlas.\n\n"
            "**References:** FREEZE CODING SCHEME V2.1, DATASET SCHEMA V2.1, CODING ORDER V1.0, SCHEMA DOCS V1.0."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health_router)
    application.include_router(campaigns_router)
    application.include_router(reports_router)
    application.include_router(sources_router)
    application.include_router(agreement_router)

    return application


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.llm_api.app.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )
