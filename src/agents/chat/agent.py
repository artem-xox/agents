from src.agents.base import BaseAgent
from src.clients.openai import OpenAIClient, OpenAIConfig, OpenAIMessage, OpenAIRequest
from src.domain.entities import ChatRequest, ChatResponse, Message, Role


class SimpleChat(BaseAgent):
    def __init__(self, openai_config: OpenAIConfig):
        super().__init__()
        self.openai_client = OpenAIClient(openai_config)

    def chat(self, request: ChatRequest) -> ChatResponse:
        self.logger.info(f"Received chat request with {len(request.messages)} messages")

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

        self.logger.info(
            f"Sending request to OpenAI with model: {openai_request.model}"
        )

        # Get response from OpenAI
        try:
            openai_response = self.openai_client.chat_completion(openai_request)
            self.logger.info(
                f"Received response from OpenAI model: {openai_response.model}"
            )

            if openai_response.usage:
                self.logger.info(f"Token usage: {openai_response.usage}")
        except Exception as e:
            self.logger.error(f"Error getting response from OpenAI: {e}")
            raise

        # Convert back to domain format
        assistant_message = Message(role=Role.ASSISTANT, text=openai_response.content)

        self.logger.info("Generated assistant response")
        return ChatResponse(messages=request.messages + [assistant_message])
