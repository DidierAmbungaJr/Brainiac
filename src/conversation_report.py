import json
import os
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field
from strands import Agent

from src.config import create_model
from src.response import ResponseCollector


class ConversationReport(BaseModel):
    """Contrat JSON stable pour le backend Django."""

    summary: str = Field(description="Résumé factuel de la conversation.")
    key_points: list[str] = Field(default_factory=list)
    customer_needs: list[str] = Field(default_factory=list)
    pain_points: list[str] = Field(default_factory=list)
    objections: list[str] = Field(default_factory=list)
    customer_questions: list[str] = Field(default_factory=list)
    recommended_next_actions: list[str] = Field(default_factory=list)
    interest_level: str = Field(description="unknown, low, medium ou high")
    lead_status: str = Field(description="new, qualified, nurturing, won ou lost")
    qualification_score: int = Field(ge=0, le=100)
    missing_information: list[str] = Field(default_factory=list)


REPORT_AGENT_PROMPT = """Tu es l'analyste commercial de Brainiac.
Tu analyses exclusivement le transcript fourni entre un commercial et un
potentiel client. Extrais les faits explicites et distingue-les des déductions.
N'invente aucune information. Si une information est absente, ajoute-la à
missing_information. Retourne uniquement le rapport conforme au schéma JSON.
Utilise une qualification prudente : interest_level doit être unknown, low,
medium ou high et lead_status doit être new, qualified, nurturing, won ou lost.
"""


def create_report_agent() -> Agent:
    """Construit le sous-agent spécialisé dans les rapports commerciaux."""
    collector = ResponseCollector()
    agent = Agent(
        model=create_model(role="reporter"),
        system_prompt=REPORT_AGENT_PROMPT,
        structured_output_model=ConversationReport,
        callback_handler=collector,
        name="conversation_reporter",
        description="Analyse un échange commercial et produit un rapport JSON Django.",
    )
    agent.response_collector = collector
    return agent


def format_transcript(messages: list[dict[str, Any]]) -> str:
    """Transforme les messages Streamlit en transcript lisible par l'agent."""
    lines = []
    for message in messages:
        role = "Commercial" if message.get("role") == "assistant" else "Client"
        content = str(message.get("content", "")).strip()
        if content:
            lines.append(f"{role}: {content}")
    return "\n".join(lines)


def generate_conversation_report(
    messages: list[dict[str, Any]] | str,
    agent: Agent | None = None,
) -> dict[str, Any]:
    """Génère un rapport JSON prêt à être envoyé à Django."""
    transcript = messages if isinstance(messages, str) else format_transcript(messages)
    if not transcript:
        raise ValueError("La conversation est vide.")

    report_agent = agent or create_report_agent()
    result = report_agent(
        "Analyse ce transcript commercial et produis le rapport demandé :\n\n"
        + transcript
    )
    structured_output = getattr(result, "structured_output", None)
    if isinstance(structured_output, ConversationReport):
        report = structured_output.model_dump(mode="json")
    elif isinstance(structured_output, BaseModel):
        report = structured_output.model_dump(mode="json")
    else:
        raise RuntimeError("Le sous-agent n'a pas retourné un rapport structuré.")

    report["generated_at"] = datetime.now(timezone.utc).isoformat()
    return report


def report_to_json(report: dict[str, Any]) -> str:
    """Sérialise le rapport avec un format directement consommable par Django."""
    return json.dumps(report, ensure_ascii=False, indent=2)


def report_to_markdown(report: dict[str, Any]) -> str:
    """Construit une version lisible du rapport pour relecture commerciale."""
    sections = [
        f"# Rapport de conversation\n\n{report.get('summary', '')}",
        _markdown_list("Points importants", report.get("key_points", [])),
        _markdown_list("Besoins du client", report.get("customer_needs", [])),
        _markdown_list("Points de douleur", report.get("pain_points", [])),
        _markdown_list("Objections", report.get("objections", [])),
        _markdown_list("Questions du client", report.get("customer_questions", [])),
        _markdown_list(
            "Prochaines actions recommandées",
            report.get("recommended_next_actions", []),
        ),
        (
            "## Qualification\n\n"
            f"- Niveau d'intérêt : {report.get('interest_level', 'unknown')}\n"
            f"- Statut : {report.get('lead_status', 'new')}\n"
            f"- Score : {report.get('qualification_score', 0)}/100"
        ),
        _markdown_list("Informations manquantes", report.get("missing_information", [])),
    ]
    return "\n\n".join(section for section in sections if section)


def _markdown_list(title: str, values: list[str]) -> str:
    if not values:
        return f"## {title}\n\nAucun élément identifié."
    return f"## {title}\n\n" + "\n".join(f"- {value}" for value in values)


__all__ = [
    "ConversationReport",
    "create_report_agent",
    "format_transcript",
    "generate_conversation_report",
    "report_to_json",
    "report_to_markdown",
]