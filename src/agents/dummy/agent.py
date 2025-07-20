from src.domain.agent import Agent
from src.domain.entities import ChatRequest, ChatResponse, Message, Role


# Placeholder: create a dummy Agent implementation for demonstration
class DummyAgent(Agent):
    def chat(self, request: ChatRequest) -> ChatResponse:
        # Echoes the last user message as assistant
        last_user_msg = next(
            (m.text for m in reversed(request.messages) if m.role == Role.USER), ""
        )
        response = Message(role=Role.ASSISTANT, text=f"Echo: {last_user_msg}")
        return ChatResponse(messages=request.messages + [response])
