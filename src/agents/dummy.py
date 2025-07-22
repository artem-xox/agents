from src.agents.base import BaseAgent
from src.domain.entities import ChatRequest, ChatResponse, Message, Role


class DummyAgent(BaseAgent):
    """
    Dummy agent that echoes the last user message as assistant.
    """

    NAME = "dummy"

    def chat(self, request: ChatRequest) -> ChatResponse:
        self.logger.info(f"Received chat request with {len(request.messages)} messages")

        # Echoes the last user message as assistant
        last_user_msg = next(
            (m.text for m in reversed(request.messages) if m.role == Role.USER), ""
        )

        self.logger.info(
            f"Echoing user message: {last_user_msg[:50]}{'...' if len(last_user_msg) > 50 else ''}"
        )

        response = Message(
            role=Role.ASSISTANT, text=f"Echo: {last_user_msg}", agent=self.NAME
        )

        self.logger.info("Generated dummy response")
        return ChatResponse(messages=request.messages + [response])
