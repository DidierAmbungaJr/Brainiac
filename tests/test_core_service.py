"""In-process coverage for the Core IA HTTP service foundation."""

import pytest
from fastapi import Body
from fastapi.testclient import TestClient
from pydantic import ValidationError

from src.config import reset_settings_cache
from src.core.exceptions import CoreError
from src.main import create_app


@pytest.fixture(autouse=True)
def valid_service_configuration(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SERVICE_NAME", "onbora-core-ia")
    monkeypatch.setenv("ENVIRONMENT", "test")
    reset_settings_cache()
    yield
    reset_settings_cache()


def test_service_exposes_health_and_openapi() -> None:
    app = create_app()

    with TestClient(app) as client:
        response = client.get("/health")
        docs_response = client.get("/docs")
        openapi_response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "onbora-core-ia",
        "environment": "test",
    }
    assert docs_response.status_code == 200
    assert openapi_response.status_code == 200
    assert openapi_response.json()["openapi"] == app.openapi()["openapi"]
    assert "/health" in app.openapi()["paths"]


@pytest.mark.parametrize("setting_name", ["SERVICE_NAME", "ENVIRONMENT"])
def test_startup_fails_before_readiness_for_missing_required_configuration(
    monkeypatch: pytest.MonkeyPatch,
    setting_name: str,
) -> None:
    monkeypatch.delenv(setting_name, raising=False)
    reset_settings_cache()

    with pytest.raises(ValidationError):
        with TestClient(create_app()):
            pass


def test_domain_errors_use_the_standard_error_envelope() -> None:
    app = create_app()

    @app.get("/domain-error")
    async def domain_error() -> None:
        raise CoreError(
            "invalid_operation",
            "The requested operation is not allowed.",
            status_code=409,
            details={"operation": "example"},
        )

    with TestClient(app) as client:
        response = client.get("/domain-error")

    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "invalid_operation",
            "message": "The requested operation is not allowed.",
            "details": {"operation": "example"},
        }
    }


def test_request_validation_errors_use_the_standard_error_envelope() -> None:
    app = create_app()

    @app.post("/validated")
    async def validated(value: int = Body()) -> dict[str, int]:
        return {"value": value}

    with TestClient(app) as client:
        response = client.post("/validated", json="provider-secret=never-expose-this")

    body = response.json()
    assert response.status_code == 422
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"] == "Request validation failed."
    diagnostics = body["error"]["details"]["errors"]
    assert isinstance(diagnostics, list)
    assert diagnostics
    assert all(set(diagnostic) == {"type", "loc", "msg"} for diagnostic in diagnostics)
    assert "provider-secret" not in response.text


@pytest.mark.parametrize(
    ("method", "path", "status_code"),
    [("get", "/missing", 404), ("post", "/health", 405)],
)
def test_http_errors_use_the_standard_error_envelope(
    method: str,
    path: str,
    status_code: int,
) -> None:
    with TestClient(create_app()) as client:
        response = getattr(client, method)(path)

    assert response.status_code == status_code
    assert response.json() == {
        "error": {
            "code": "http_error",
            "message": "The requested HTTP operation could not be completed.",
            "details": {},
        }
    }


def test_unexpected_errors_are_redacted_in_the_standard_envelope() -> None:
    app = create_app()

    @app.get("/unexpected-error")
    async def unexpected_error() -> None:
        raise RuntimeError("provider-secret=never-expose-this")

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/unexpected-error")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "internal_error",
            "message": "An unexpected error occurred.",
            "details": {},
        }
    }
