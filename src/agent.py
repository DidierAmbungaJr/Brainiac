import os

from strands import Agent
from strands.session.file_session_manager import FileSessionManager

from src.config import create_model
from src.tools.custom_tools import TOOLS

SYSTEM_PROMPT = """Tu es un assistant utile, précis et concis.
Réponds en français sauf si l'utilisateur demande une autre langue.
Utilise les outils disponibles lorsqu'une information doit être calculée ou vérifiée.
Ne prétends pas avoir utilisé un outil si ce n'est pas le cas.
"""


def create_agent(
    session_id: str | None = None,
    storage_dir: str | None = None,
) -> Agent:
    """Crée l'agent avec son modèle, ses outils et ses instructions."""
    session_manager = FileSessionManager(
        session_id=session_id or os.getenv("AGENT_SESSION_ID", "user_session_123"),
        storage_dir=storage_dir or os.getenv("AGENT_SESSIONS_DIR", "./sessions"),
    )
    return Agent(
        model=create_model(),
        tools=TOOLS,
        system_prompt=SYSTEM_PROMPT,
        session_manager=session_manager,
        load_tools_from_directory=True,
    )