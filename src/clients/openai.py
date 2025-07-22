import time
from dataclasses import dataclass

import openai

from src.infra.logger import get_logger


@dataclass
class OpenAIConfig:
    api_key: str
    model: str
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
    functions: list[dict] | None = None
    function_call: str | dict | None = None


@dataclass
class OpenAIResponse:
    content: str
    model: str
    usage: dict
    function_call: dict | None = None


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

                # Prepare request parameters
                request_params = {
                    "model": request.model,
                    "messages": messages,  # type: ignore
                    "temperature": request.temperature,
                }

                if request.max_tokens:
                    request_params["max_tokens"] = request.max_tokens
                if request.functions:
                    request_params["functions"] = request.functions
                if request.function_call:
                    request_params["function_call"] = request.function_call

                response = self.client.chat.completions.create(**request_params)

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

        message = response.choices[0].message
        content = message.content
        function_call = (
            message.function_call.model_dump() if message.function_call else None
        )

        if content is None and function_call is None:
            self.logger.error("OpenAI response has no content or function call")
            raise ValueError("OpenAI response has no content or function call")

        if content:
            self.logger.info(f"Response content length: {len(content)} characters")
        if function_call:
            self.logger.info(
                f"Function call detected: {function_call.get('name', 'unknown')}"
            )

        return OpenAIResponse(
            content=content or "",
            model=response.model,
            usage=response.usage.model_dump() if response.usage else {},
            function_call=function_call,
        )
