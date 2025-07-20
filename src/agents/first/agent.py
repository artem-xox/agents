import os
from dataclasses import dataclass
from typing import Optional

import openai

from src.domain.agent import Agent
from src.domain.entities import ChatRequest, ChatResponse, Message, Role


@dataclass
class OpenAIConfig:
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: Optional[int] = None


@dataclass
class OpenAIMessage:
    role: str
    content: str


@dataclass
class OpenAIRequest:
    model: str
    messages: list[OpenAIMessage]
    temperature: float = 0.7
    max_tokens: Optional[int] = None


@dataclass
class OpenAIResponse:
    content: str
    model: str
    usage: dict


class OpenAIClient:
    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = openai.OpenAI(api_key=config.api_key)

    def chat_completion(self, request: OpenAIRequest) -> OpenAIResponse:
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        response = self.client.chat.completions.create(
            model=request.model,
            messages=messages,  # type: ignore
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI response content is None")

        return OpenAIResponse(
            content=content,
            model=response.model,
            usage=response.usage.model_dump() if response.usage else {},
        )


class FirstAgent(Agent):
    def __init__(self, openai_config: OpenAIConfig):
        self.openai_client = OpenAIClient(openai_config)

    def chat(self, request: ChatRequest) -> ChatResponse:
        # Convert domain messages to OpenAI format
        openai_messages = []
        for msg in request.messages:
            openai_messages.append(OpenAIMessage(role=msg.role, content=msg.text))

        # Create OpenAI request
        openai_request = OpenAIRequest(
            model=self.openai_client.config.model,
            messages=openai_messages,
            temperature=self.openai_client.config.temperature,
            max_tokens=self.openai_client.config.max_tokens,
        )

        # Get response from OpenAI
        openai_response = self.openai_client.chat_completion(openai_request)

        # Convert back to domain format
        assistant_message = Message(role=Role.ASSISTANT, text=openai_response.content)

        return ChatResponse(messages=request.messages + [assistant_message])
