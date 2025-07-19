import abc

from src.domain.entities import ChatRequest, ChatResponse


class Agent(abc.ABC):
    """Abstract base class for all agents."""

    @abc.abstractmethod
    def chat(self, request: ChatRequest) -> ChatResponse:
        raise NotImplementedError
