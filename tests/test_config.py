import builtins

import pytest

from src import config
from src import main
from src import multi_agent


def clear_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)


def test_create_model_requires_a_gemini_credential_before_provider_construction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clear_credentials(monkeypatch)

    def fail_if_constructed(**_: object) -> object:
        raise AssertionError("GeminiModel must not be constructed without a credential")

    monkeypatch.setattr(config, "GeminiModel", fail_if_constructed)

    with pytest.raises(RuntimeError, match="GOOGLE_API_KEY ou GEMINI_API_KEY est absente"):
        config.create_model()


def test_cli_surfaces_the_missing_credential_before_an_agent_call(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    clear_credentials(monkeypatch)
    monkeypatch.setenv("BRAINIAC_AGENT_MODE", "simple")
    monkeypatch.setattr(main, "create_agent", config.create_model)

    main.main()

    assert "Configuration invalide" in capsys.readouterr().out


def test_cli_reaches_the_existing_poc_loop_with_an_injected_agent(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setenv("BRAINIAC_AGENT_MODE", "simple")
    monkeypatch.setattr(main, "create_agent", lambda: object())
    monkeypatch.setattr(builtins, "input", lambda _: "quit")

    main.main()

    assert "Brainiac est prêt" in capsys.readouterr().out


def test_default_hierarchical_cli_factory_constructs_without_an_llm_call(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    clear_credentials(monkeypatch)
    monkeypatch.setenv("GOOGLE_API_KEY", "baseline-test-key")

    team = multi_agent.create_team(session_id="baseline-smoke", storage_dir=str(tmp_path))

    assert team.name == "supervisor"


@pytest.mark.parametrize(
    ("role", "environment_name"),
    [
        ("supervisor", "GEMINI_SUPERVISOR_MODEL"),
        ("researcher", "GEMINI_RESEARCHER_MODEL"),
        ("reporter", "GEMINI_REPORTER_MODEL"),
    ],
)
def test_create_model_prefers_google_key_and_uses_role_override(
    monkeypatch: pytest.MonkeyPatch,
    role: str,
    environment_name: str,
) -> None:
    captured: dict[str, object] = {}

    def fake_gemini_model(**kwargs: object) -> object:
        captured.update(kwargs)
        return object()

    monkeypatch.setenv("GOOGLE_API_KEY", "google-key")
    monkeypatch.setenv("GEMINI_API_KEY", "fallback-key")
    monkeypatch.setenv("GEMINI_MODEL", "default-model")
    monkeypatch.setenv(environment_name, f"{role}-model")
    monkeypatch.setenv("GEMINI_TEMPERATURE", "0.3")
    monkeypatch.setenv("GEMINI_MAX_OUTPUT_TOKENS", "512")
    monkeypatch.setattr(config, "GeminiModel", fake_gemini_model)

    config.create_model(role=role)

    assert captured["model_id"] == f"{role}-model"
    assert captured["client_args"] == {"api_key": "google-key"}
    assert captured["params"] == {
        "temperature": 0.3,
        "max_output_tokens": 512,
        "top_p": 0.9,
        "top_k": 40,
    }


def test_create_model_uses_gemini_key_when_google_key_is_absent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    clear_credentials(monkeypatch)
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-key")
    monkeypatch.setattr(config, "GeminiModel", lambda **kwargs: captured.update(kwargs))

    config.create_model()

    assert captured["client_args"] == {"api_key": "gemini-key"}


@pytest.mark.parametrize(
    ("role", "environment_name"),
    [
        ("supervisor", "GEMINI_SUPERVISOR_MODEL"),
        ("researcher", "GEMINI_RESEARCHER_MODEL"),
        ("reporter", "GEMINI_REPORTER_MODEL"),
    ],
)
def test_empty_role_override_falls_back_to_the_default_model(
    monkeypatch: pytest.MonkeyPatch,
    role: str,
    environment_name: str,
) -> None:
    captured: dict[str, object] = {}
    monkeypatch.setenv("GOOGLE_API_KEY", "google-key")
    monkeypatch.setenv("GEMINI_MODEL", "default-model")
    monkeypatch.setenv(environment_name, "")
    monkeypatch.setattr(config, "GeminiModel", lambda **kwargs: captured.update(kwargs))

    config.create_model(role=role)

    assert captured["model_id"] == "default-model"
