"""Tests for fail-fast Core IA service settings."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from src import config
from src.config import get_settings, reset_settings_cache


@pytest.fixture(autouse=True)
def clear_settings_cache() -> None:
    reset_settings_cache()
    yield
    reset_settings_cache()


def test_settings_loads_documented_service_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SERVICE_NAME", "onbora-core-ia")
    monkeypatch.setenv("ENVIRONMENT", "test")

    settings = get_settings()

    assert settings.service_name == "onbora-core-ia"
    assert settings.environment == "test"


@pytest.mark.parametrize(
    "service_name",
    [None, "", "   ", "a" * 101],
)
def test_settings_rejects_missing_blank_or_overlength_service_name(
    monkeypatch: pytest.MonkeyPatch,
    service_name: str | None,
) -> None:
    monkeypatch.setenv("ENVIRONMENT", "test")
    if service_name is None:
        monkeypatch.delenv("SERVICE_NAME", raising=False)
    else:
        monkeypatch.setenv("SERVICE_NAME", service_name)

    with pytest.raises(ValidationError):
        get_settings()


def test_settings_rejects_missing_or_unsupported_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SERVICE_NAME", "onbora-core-ia")
    monkeypatch.setenv("ENVIRONMENT", "staging")

    with pytest.raises(ValidationError):
        get_settings()


def test_settings_load_from_configured_env_file_outside_project_directory(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    environment_file = tmp_path / ".env"
    environment_file.write_text(
        "SERVICE_NAME=from-temp-env\nENVIRONMENT=test\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("SERVICE_NAME", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    monkeypatch.setattr(config, "PROJECT_ENV_FILE", environment_file)
    (tmp_path / "outside-project").mkdir()
    monkeypatch.chdir(tmp_path / "outside-project")

    settings = get_settings()

    assert settings.service_name == "from-temp-env"
    assert settings.environment == "test"
