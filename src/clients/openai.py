import os
import time
from dataclasses import dataclass

import openai


@dataclass
class OpenAIConfig:
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = "gpt-4.1-2025-04-14"
    temperature: float = 0.7
    max_tokens: int | None = None


@dataclass
class OpenAIMessage:
    role: str
    content: str


@dataclass
class OpenAIRequest:
    model: str
    messages: list[OpenAIMessage]
    temperature: float = 0.7
    max_tokens: int | None = None


@dataclass
class OpenAIResponse:
    content: str
    model: str
    usage: dict


class OpenAIClient:
    """
    OpenAI client with retry mechanism.
    """

    MAX_RETRIES = 3

    def __init__(self, config: OpenAIConfig):
        self.config = config

        self.client = openai.OpenAI(api_key=config.api_key)

    def chat_completion(self, request: OpenAIRequest) -> OpenAIResponse:
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=request.model,
                    messages=messages,  # type: ignore
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                )
                break
            except Exception:
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(1.5 * (attempt + 1))
                else:
                    raise

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI response content is None")

        return OpenAIResponse(
            content=content,
            model=response.model,
            usage=response.usage.model_dump() if response.usage else {},
        )
