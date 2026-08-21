import os

from strands import Agent
from strands.session.file_session_manager import FileSessionManager

from src.config import create_model
from src.conversation_report import ConversationReport, create_report_agent
from src.response import ResponseCollector
from src.tools.custom_tools import TOOLS

RESEARCHER_PROMPT = """Tu es l'agent de recherche specialise de Brainiac.
Analyse la demande qui t'est deleguee, utilise les outils disponibles quand ils
sont pertinents, puis retourne une synthese factuelle et structuree au superviseur.
Signale clairement les informations manquantes et ne presente jamais une
hypothese comme un fait etabli.
"""

SUPERVISOR_PROMPT = """Tu es le superviseur de Brainiac.
Tu reponds en francais, de facon precise et concise.
Tu es responsable de la reponse finale et de la coordination des outils.
Delegue au chercheur les demandes qui necessitent une analyse, une verification
ou une synthese. Donne-lui une consigne complete, puis controle et reformule son
resultat avant de repondre a l'utilisateur.
Delegue au rapporteur commercial les transcripts de conversations qui doivent
etre transformes en rapport structure pour un CRM ou un backend Django.
Pour une question simple, reponds directement sans deleguer.
Ne pretends jamais qu'une recherche ou une action a ete effectuee si ce n'est pas
le cas.
"""


def create_researcher() -> Agent:
    """Construit le sous-agent specialise dans la recherche et la verification."""
    collector = ResponseCollector()
    agent = Agent(
        model=create_model(role="researcher"),
        tools=TOOLS,
        system_prompt=RESEARCHER_PROMPT,
        callback_handler=collector,
        name="researcher",
        description="Recherche, verifie et synthetise les informations deleguees.",
        load_tools_from_directory=True,
    )
    agent.response_collector = collector
    return agent


def create_supervisor(
    session_id: str | None = None,
    storage_dir: str | None = None,
) -> Agent:
    """Construit le superviseur et lui expose le chercheur comme outil."""
    researcher = create_researcher()
    researcher_tool = researcher.as_tool(
        name="delegate_to_researcher",
        description=(
            "Delegue une question au chercheur specialise. Utilise cet outil "
            "pour verifier ou synthetiser des informations avant de repondre."
        ),
    )
    report_agent = create_report_agent()
    report_tool = report_agent.as_tool(
        name="delegate_to_conversation_reporter",
        description=(
            "Analyse un transcript entre commercial et client et retourne un "
            "rapport structure avec qualification et prochaines actions."
        ),
    )
    session_manager = FileSessionManager(
        session_id=session_id or os.getenv("AGENT_SESSION_ID", "user_session_123"),
        storage_dir=storage_dir or os.getenv("AGENT_SESSIONS_DIR", "./sessions"),
    )
    collector = ResponseCollector()
    agent = Agent(
        model=create_model(role="supervisor"),
        tools=[*TOOLS, researcher_tool, report_tool],
        system_prompt=SUPERVISOR_PROMPT,
        callback_handler=collector,
        name="supervisor",
        description="Supervise les demandes et delegue les recherches specialisees.",
        session_manager=session_manager,
        load_tools_from_directory=True,
    )
    agent.response_collector = collector
    return agent


def create_report_orchestrator() -> Agent:
    """Construit l'orchestrateur qui délègue le rapport au sous-agent métier."""
    reporter = create_report_agent()
    reporter_tool = reporter.as_tool(
        name="delegate_to_conversation_reporter",
        description=(
            "Analyse le transcript d'une visite commerciale et retourne les "
            "faits, besoins, objections et actions recommandées."
        ),
    )
    collector = ResponseCollector()
    agent = Agent(
        model=create_model(role="supervisor"),
        tools=[reporter_tool],
        system_prompt=(
            "Tu es l'orchestrateur du reporting commercial. Délègue toujours "
            "le transcript au rapporteur commercial, vérifie son résultat et "
            "retourne uniquement le schéma ConversationReport."
        ),
        structured_output_model=ConversationReport,
        callback_handler=collector,
        name="report_orchestrator",
        description="Orchestre la production de rapports commerciaux structurés.",
    )
    agent.response_collector = collector
    return agent


def create_team(
    session_id: str | None = None,
    storage_dir: str | None = None,
) -> Agent:
    """Point d'entree de l'architecture multi-agent hierarchique."""
    return create_supervisor(session_id=session_id, storage_dir=storage_dir)


__all__ = [
    "create_researcher",
    "create_report_orchestrator",
    "create_supervisor",
    "create_team",
]