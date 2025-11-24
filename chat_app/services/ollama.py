import httpx
import json
import logging
from typing import AsyncGenerator
from chat_app.core.interfaces import LLMProvider
from chat_app.core.models import ChatSession

logger = logging.getLogger("OllamaService")


class OllamaService(LLMProvider):
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api/chat"
        self.tags_url = f"{self.base_url}/api/tags"

    async def get_models(self) -> list[str]:
        """Fetches the list of available models from Ollama."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.tags_url)
                response.raise_for_status()
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
        except Exception as e:
            logger.error(f"Failed to fetch models: {e}")
            return []

    async def stream_chat(self, session: ChatSession) -> AsyncGenerator[str, None]:
        """
        Streams the response from Ollama for the given chat session.
        """
        # Convert internal messages to Ollama format
        messages_payload = [
            {
                "role": msg.role.value,
                "content": msg.content,
                "images": msg.images if msg.images else None,
            }
            for msg in session.messages
        ]

        payload = {"model": session.model, "messages": messages_payload, "stream": True}

        try:
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST", self.api_url, json=payload
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line:
                            continue

                        try:
                            data = json.loads(line)
                            if "message" in data and "content" in data["message"]:
                                yield data["message"]["content"]

                            if data.get("done", False):
                                break
                        except json.JSONDecodeError:
                            logger.error(f"Failed to decode JSON: {line}")

        except httpx.ConnectError:
            yield "Error: Could not connect to Ollama. Is it running?"
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            yield f"Error: {str(e)}"
