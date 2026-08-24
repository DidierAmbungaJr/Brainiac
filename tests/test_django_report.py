from types import SimpleNamespace

import requests

from src.django_report import send_django_report


def test_send_django_report_posts_the_report_and_returns_success() -> None:
    captured: dict[str, object] = {}

    def fake_post(_: str, **kwargs: object) -> SimpleNamespace:
        captured.update(kwargs)
        return SimpleNamespace(ok=True, status_code=201)

    delivery = send_django_report(
        "https://django.example.test/reports",
        {"summary": "POC report"},
        post=fake_post,
    )

    assert delivery.success is True
    assert captured == {
        "json": {"summary": "POC report"},
        "timeout": 20,
    }


def test_send_django_report_reports_an_actionable_connection_failure() -> None:
    def unavailable_post(_: str, **__: object) -> object:
        raise requests.ConnectionError("connection refused")

    delivery = send_django_report(
        "https://django.example.test/reports",
        {"summary": "POC report"},
        post=unavailable_post,
    )

    assert delivery.success is False
    assert "DJANGO_REPORT_URL" in delivery.message
    assert "service est disponible" in delivery.message
