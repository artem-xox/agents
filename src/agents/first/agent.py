from src.clients.openai import OpenAIClient, OpenAIConfig, OpenAIMessage, OpenAIRequest
from src.domain.agent import Agent
from src.domain.entities import ChatRequest, ChatResponse, Message, Role


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
