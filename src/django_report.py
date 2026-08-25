from dataclasses import dataclass
from typing import Any, Callable

import requests


@dataclass(frozen=True)
class DjangoReportDelivery:
    success: bool
    message: str


def send_django_report(
    url: str,
    report: dict[str, Any],
    *,
    post: Callable[..., Any] = requests.post,
) -> DjangoReportDelivery:
    """Send a POC report to Django and return an actionable UI message."""
    try:
        response = post(url, json=report, timeout=20)
    except requests.RequestException:
        return DjangoReportDelivery(
            success=False,
            message=(
                "Impossible de joindre le backend Django. Vérifiez "
                "DJANGO_REPORT_URL et que le service est disponible."
            ),
        )

    if response.ok:
        return DjangoReportDelivery(success=True, message="Rapport envoyé au backend Django.")
    return DjangoReportDelivery(
        success=False,
        message=f"Le backend a répondu {response.status_code}.",
    )
