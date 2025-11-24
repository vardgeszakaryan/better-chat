from abc import ABC, abstractmethod
from typing import AsyncGenerator
from .models import ChatSession


class LLMProvider(ABC):
    """Abstract base class for LLM providers (Ollama, etc)."""

    @abstractmethod
    async def stream_chat(self, session: ChatSession) -> AsyncGenerator[str, None]:
        """Stream response from the LLM based on the session history."""
        pass
