"""Health response contract."""

from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """The readiness state of the Core IA service."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"]
    service: str
    environment: str
