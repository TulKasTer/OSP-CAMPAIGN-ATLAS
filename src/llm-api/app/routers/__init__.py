"""FastAPI routers for OSP Campaign Atlas LLM API."""

from .health import router as health_router
from .campaigns import router as campaigns_router
from .reports import router as reports_router
from .sources import router as sources_router
from .agreement import router as agreement_router

__all__ = [
    "health_router",
    "campaigns_router",
    "reports_router",
    "sources_router",
    "agreement_router",
]
