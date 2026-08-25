"""Service health resource."""

from typing import Annotated

from fastapi import APIRouter, Depends

from src.config import Settings, get_settings
from src.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Check service readiness")
async def get_health(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthResponse:
    """Report the service's own readiness without probing providers."""

    return HealthResponse(
        status="ok",
        service=settings.service_name,
        environment=settings.environment,
    )
