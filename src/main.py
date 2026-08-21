import os

from src.agent import create_agent
from src.multi_agent import create_team
from src.response import invoke_agent


def main() -> None:
    try:
        factory = create_agent if os.getenv("BRAINIAC_AGENT_MODE") == "simple" else create_team
        agent = factory()
    except RuntimeError as error:
        print(f"Configuration invalide : {error}")
        return

    print("Brainiac est prêt. Écrivez 'quit' pour arrêter.")

    while True:
        try:
            message = input("Vous : ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if message.lower() in {"quit", "exit", "q"}:
            break
        if not message:
            continue

        try:
            output = invoke_agent(agent, message)
        except Exception as error:
            print(f"Erreur pendant l'appel de l'agent : {error}")
            continue
        if output.thinking:
            print(f"Traitement :\n{output.thinking}")
        print(f"Agent :\n{output.response}")


if __name__ == "__main__":
    main()