from src.agent import create_agent


def main() -> None:
    try:
        agent = create_agent()
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
            response = agent(message)
        except Exception as error:
            print(f"Erreur pendant l'appel de l'agent : {error}")
            continue
        print(f"Agent : {response}")


if __name__ == "__main__":
    main()