import os

from dotenv import load_dotenv
from strands.models.gemini import GeminiModel

load_dotenv()


def create_model() -> GeminiModel:
    """Construit le modèle Gemini à partir des variables d'environnement."""
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY est absente. Copiez .env.example vers .env et ajoutez votre clé."
        )

    return GeminiModel(
        model_id=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        client_args={"api_key": api_key},
        params={
            "temperature": float(os.getenv("GEMINI_TEMPERATURE", "0.7")),
            "max_output_tokens": int(os.getenv("GEMINI_MAX_OUTPUT_TOKENS", "2048")),
            "top_p": 0.9,
            "top_k": 40,
        },
        use_native_token_count=True,
    )