from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    id: str = Field(
        default_factory=lambda: str(datetime.now().timestamp()),
        description="Unique message ID",
    )
    role: Role = Field(..., description="Role of the sender")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now)
    images: Optional[list[str]] = Field(
        default=None, description="Base64 encoded images"
    )


class ChatSession(BaseModel):
    messages: list[ChatMessage] = Field(default_factory=list)
    model: str = Field(default="llama2", description="Ollama model to use")
