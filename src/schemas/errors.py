"""Shared public API error contract."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ErrorDetail(BaseModel):
    """A client-safe error description."""

    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    """The stable envelope returned for all API failures."""

    model_config = ConfigDict(extra="forbid")

    error: ErrorDetail
