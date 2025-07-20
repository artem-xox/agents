import os
import time
from dataclasses import dataclass

import openai

from src.infra.logger import get_logger


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
        self.logger = get_logger(__name__)
        self.client = openai.OpenAI(api_key=config.api_key)
        self.logger.info(f"Initialized OpenAI client with model: {config.model}")

    def chat_completion(self, request: OpenAIRequest) -> OpenAIResponse:
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        self.logger.info(
            f"Starting chat completion request with {len(messages)} messages"
        )

        for attempt in range(self.MAX_RETRIES):
            try:
                self.logger.info(
                    f"Attempt {attempt + 1}/{self.MAX_RETRIES} to call OpenAI API"
                )

                response = self.client.chat.completions.create(
                    model=request.model,
                    messages=messages,  # type: ignore
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                )

                self.logger.info(
                    f"Successfully received response from OpenAI on attempt {attempt + 1}"
                )
                break
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.MAX_RETRIES - 1:
                    sleep_time = 1.5 * (attempt + 1)
                    self.logger.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    self.logger.error(
                        f"All {self.MAX_RETRIES} attempts failed. Last error: {e}"
                    )
                    raise

        content = response.choices[0].message.content
        if content is None:
            self.logger.error("OpenAI response content is None")
            raise ValueError("OpenAI response content is None")

        self.logger.info(f"Response content length: {len(content)} characters")

        return OpenAIResponse(
            content=content,
            model=response.model,
            usage=response.usage.model_dump() if response.usage else {},
        )
