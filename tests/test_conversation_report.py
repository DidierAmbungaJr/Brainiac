import json
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from src import conversation_report
from src.conversation_report import (
    ConversationReport,
    format_transcript,
    generate_conversation_report,
    report_to_json,
    report_to_markdown,
)


def make_report() -> ConversationReport:
    return ConversationReport(
        summary="Customer needs a mobile plan for a growing team.",
        key_points=["Fifteen employees require service."],
        customer_needs=["Shared mobile plan"],
        pain_points=["Current coverage is unreliable."],
        objections=["Budget approval is pending."],
        customer_questions=["Is roaming included?"],
        recommended_next_actions=["Send a priced proposal."],
        interest_level="medium",
        lead_status="qualified",
        qualification_score=70,
        missing_information=["Target start date"],
    )


class FakeReportAgent:
    def __init__(self, structured_output: object) -> None:
        self.structured_output = structured_output
        self.prompts: list[str] = []

    def __call__(self, prompt: str) -> SimpleNamespace:
        self.prompts.append(prompt)
        return SimpleNamespace(structured_output=self.structured_output)


def test_conversation_report_validates_required_fields_and_score() -> None:
    report = make_report()

    assert report.qualification_score == 70
    with pytest.raises(ValidationError):
        ConversationReport.model_validate({"summary": "Missing required fields"})
    with pytest.raises(ValidationError):
        ConversationReport.model_validate(
            {
                **make_report().model_dump(),
                "qualification_score": 101,
            }
        )


def test_format_transcript_maps_roles_trims_content_and_preserves_order() -> None:
    messages = [
        {"role": "user", "content": "  Bonjour  "},
        {"role": "assistant", "content": " Salut "},
        {"role": "assistant", "content": "   "},
        {"role": "system", "content": " Need more information. "},
    ]

    assert format_transcript(messages) == (
        "Client: Bonjour\n"
        "Commercial: Salut\n"
        "Client: Need more information."
    )


def test_generate_report_uses_injected_fake_and_serializes_utc_timestamp(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_agent = FakeReportAgent(make_report())

    def fail_if_called() -> object:
        raise AssertionError("create_report_agent must not be called when a fake is injected")

    monkeypatch.setattr(conversation_report, "create_report_agent", fail_if_called)

    result = generate_conversation_report(
        [
            {"role": "user", "content": "We need service."},
            {"role": "assistant", "content": "I can prepare an offer."},
        ],
        agent=fake_agent,  # type: ignore[arg-type]
    )

    assert len(fake_agent.prompts) == 1
    assert "Client: We need service." in fake_agent.prompts[0]
    assert "Commercial: I can prepare an offer." in fake_agent.prompts[0]
    generated_at = datetime.fromisoformat(result["generated_at"])
    assert generated_at.tzinfo == timezone.utc
    assert result["summary"] == make_report().summary
    assert json.loads(report_to_json(result)) == result


@pytest.mark.parametrize("messages", [[], "", "   "])
def test_generate_report_rejects_empty_transcript(messages: list[dict[str, str]] | str) -> None:
    with pytest.raises(ValueError, match="La conversation est vide"):
        generate_conversation_report(messages, agent=FakeReportAgent(make_report()))  # type: ignore[arg-type]


@pytest.mark.parametrize("structured_output", [None, {"summary": "not a model"}])
def test_generate_report_rejects_missing_or_non_pydantic_output(structured_output: object) -> None:
    with pytest.raises(RuntimeError, match="rapport structuré"):
        generate_conversation_report(
            "Client: Bonjour",
            agent=FakeReportAgent(structured_output),  # type: ignore[arg-type]
        )


def test_report_to_markdown_renders_qualification_and_empty_sections() -> None:
    report = make_report().model_dump(mode="json")
    report["objections"] = []

    rendered = report_to_markdown(report)

    assert "## Objections\n\nAucun élément identifié." in rendered
    assert "- Niveau d'intérêt : medium" in rendered
    assert "- Score : 70/100" in rendered
