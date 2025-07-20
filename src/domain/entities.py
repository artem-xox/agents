from dataclasses import dataclass


class Role:
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"


@dataclass
class Message:
    role: Role
    text: str


@dataclass
class ChatRequest:
    messages: list[Message]


@dataclass
class ChatResponse:
    messages: list[Message]
