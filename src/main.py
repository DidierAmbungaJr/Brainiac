"""ASGI entry point for the Core IA service."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.api.router import router
from src.config import get_settings
from src.core.exceptions import CoreError
from src.schemas.errors import ErrorDetail, ErrorResponse


def _error_response(
    *, status_code: int, code: str, message: str, details: dict[str, object] | None = None
) -> JSONResponse:
    """Create a response that complies with the single public error contract."""

    payload = ErrorResponse(
        error=ErrorDetail(code=code, message=message, details=details or {})
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump(mode="json"))


def _validation_details(error: RequestValidationError) -> list[dict[str, object]]:
    """Keep validation diagnostics structured without reflecting request input."""

    return [
        {
            "type": item["type"],
            "loc": list(item["loc"]),
            "msg": item["msg"],
        }
        for item in error.errors()
    ]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Validate settings before the application is ready to handle traffic."""

    get_settings()
    yield


def create_app() -> FastAPI:
    """Assemble the side-effect-free Core IA ASGI application."""

    app = FastAPI(
        title="Onbora Core IA",
        version="0.1.0",
        description="The independently runnable Core IA HTTP service.",
        lifespan=lifespan,
    )
    app.include_router(router)

    @app.exception_handler(CoreError)
    async def handle_core_error(_: Request, error: CoreError) -> JSONResponse:
        return _error_response(
            status_code=error.status_code,
            code=error.code,
            message=error.message,
            details=error.details,
        )

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation_error(
        _: Request, error: RequestValidationError
    ) -> JSONResponse:
        return _error_response(
            status_code=422,
            code="validation_error",
            message="Request validation failed.",
            details={"errors": _validation_details(error)},
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_error(_: Request, error: StarletteHTTPException) -> JSONResponse:
        return _error_response(
            status_code=error.status_code,
            code="http_error",
            message="The requested HTTP operation could not be completed.",
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(_: Request, __: Exception) -> JSONResponse:
        return _error_response(
            status_code=500,
            code="internal_error",
            message="An unexpected error occurred.",
        )

    return app


app = create_app()
