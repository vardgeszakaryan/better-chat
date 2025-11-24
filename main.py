import argparse
from chat_app.client.app import BetterChatApp


def main():
    parser = argparse.ArgumentParser(description="Better Chat - Terminal Ollama Client")
    parser.add_argument(
        "--url", default="http://localhost:11434", help="Ollama API URL"
    )
    parser.add_argument("--model", default="llama2", help="Ollama Model to use")
    args = parser.parse_args()

    app = BetterChatApp(base_url=args.url, model=args.model)
    app.run()


if __name__ == "__main__":
    main()
