from dataclasses import dataclass
import re
from typing import Any


@dataclass
class AgentResponse:
    """Sortie d'agent séparant les détails de traitement de la réponse finale."""

    response: str
    thinking: str = ""


class ResponseCollector:
    """Collecte les fragments de streaming sans les écrire dans le terminal."""

    def __init__(self) -> None:
        self.thinking_parts: list[str] = []

    def reset(self) -> None:
        self.thinking_parts.clear()

    def __call__(self, **event: Any) -> None:
        reasoning_text = event.get("reasoningText")
        if reasoning_text:
            self.thinking_parts.append(str(reasoning_text))

    @property
    def thinking(self) -> str:
        return "".join(self.thinking_parts).strip()


def _text_from_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("text", "content", "summary"):
            if key in value:
                text = _text_from_value(value[key])
                if text:
                    return text
    if isinstance(value, list):
        return "\n".join(filter(None, (_text_from_value(item) for item in value)))
    return ""


def _split_labeled_reasoning(text: str) -> tuple[str, str]:
    """Sépare un raisonnement explicitement marqué dans le texte final."""
    label_prefix = r"[*_#\s]*"
    match = re.search(
        rf"(?is)(?:^|\n){label_prefix}(?:raisonnement|réflexion|thinking)"
        rf"{label_prefix}:{label_prefix}",
        text,
    )
    if not match:
        return text.strip(), ""

    start = match.end()
    answer_match = re.search(
        rf"(?is)\n{label_prefix}(?:réponse finale|réponse|final answer)"
        rf"{label_prefix}:{label_prefix}",
        text[start:],
    )
    if not answer_match:
        return text.strip(), text[start:].strip()

    thinking = text[start : start + answer_match.start()].strip()
    response = text[start + answer_match.end() :].strip()
    return response, thinking


def split_agent_response(result: Any) -> AgentResponse:
    """Extrait une réponse Strands sans concaténer deux fois son contenu."""
    if isinstance(result, str):
        return AgentResponse(response=result.strip())

    message = getattr(result, "message", None)
    content = message.get("content", []) if isinstance(message, dict) else []
    response_parts: list[str] = []
    thinking_parts: list[str] = []

    for block in content:
        if not isinstance(block, dict):
            continue
        if "text" in block:
            response_parts.append(_text_from_value(block["text"]))
        for key in ("reasoningContent", "reasoning", "thinking"):
            if key in block:
                thinking_parts.append(_text_from_value(block[key]))

    response = "\n".join(filter(None, response_parts)).strip()
    thinking = "\n".join(filter(None, thinking_parts)).strip()
    if not response:
        response = str(result).strip()
    response, labeled_thinking = _split_labeled_reasoning(response)
    if not thinking:
        thinking = labeled_thinking
    return AgentResponse(response=response, thinking=thinking)


def invoke_agent(agent: Any, prompt: str) -> AgentResponse:
    """Invoque un agent silencieusement et retourne une sortie normalisee."""
    collector = getattr(agent, "response_collector", None)
    if collector is not None:
        collector.reset()
    output = split_agent_response(agent(prompt))
    if not output.thinking and collector is not None:
        output.thinking = collector.thinking
    return output


__all__ = ["AgentResponse", "ResponseCollector", "invoke_agent", "split_agent_response"]