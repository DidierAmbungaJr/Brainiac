from datetime import datetime

from strands import tool


@tool
def current_time() -> str:
    """Retourne la date et l'heure locales actuelles."""
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


@tool
def calculate_age(birth_year: int, current_year: int) -> int:
    """Calcule un âge approximatif à partir de deux années."""
    return current_year - birth_year


@tool
def get_user_profile(user_id: str) -> str:
    """Récupère un profil utilisateur de démonstration à partir de son identifiant."""
    return f"Profil utilisateur [ID: {user_id}] : Statut=Actif, Plan=Premium, Région=FR"


TOOLS = [current_time, calculate_age, get_user_profile]

__all__ = ["TOOLS", "calculate_age", "current_time", "get_user_profile"]