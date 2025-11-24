# Better Chat

A scalable and user-friendly terminal-based chat application for interacting with local language models through the Ollama service. Built with Python and the [Textual](https://textual.textualize.io/) framework.

![Better Chat Screenshot](https://raw.githubusercontent.com/user/repo/main/screenshot.png) <!--- Placeholder for screenshot -->

## Features

- **Connect to any Ollama instance:** Specify the URL of your Ollama service.
- **Model Selection:** Lists all available models from your Ollama instance and allows you to switch between them.
- **Streaming Responses:** Receives and displays model responses in real-time.
- **Intuitive Terminal UI:** A clean and responsive user interface built with Textual.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai/) installed and running.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/better-chat.git
    cd better-chat
    ```

2.  **Install the dependencies:**
    ```bash
    pip install .
    ```

### Running the Application

To run the application, use the following command:

```bash
better-chat
```

You can also specify the Ollama service URL and the model to use with command-line arguments:

```bash
better-chat --url http://localhost:11434 --model llama2
```

- `--url`: The URL of your Ollama API instance (default: `http://localhost:11434`).
- `--model`: The name of the model to use (default: `llama2`).

## Architecture

The application is structured into three main components:

- **`chat_app/client`**: Contains the Textual application, including the UI components for the chat display, input area, and model list.
- **`chat_app/core`**: Defines the core data models and interfaces used throughout the application, such as `ChatSession` and `ChatMessage`.
- **`chat_app/services`**: Includes the `OllamaService`, which is responsible for all communication with the Ollama API, such as fetching models and streaming chat responses.

## Development

To install the development dependencies, run:
```bash
pip install -e ".[dev]"
```
