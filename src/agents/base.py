from abc import ABC, abstractmethod

from src.domain.agent import Agent
from src.domain.entities import ChatRequest, ChatResponse
from src.infra.logger import get_logger


class BaseAgent(Agent, ABC):
    """
    Base agent class with common logging functionality.
    """

    def __init__(self):
        self.logger = get_logger(self.__class__.__module__)
        self.logger.info(f"Initialized {self.__class__.__name__}")

    @abstractmethod
    def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Process a chat request and return a response.

        Args:
            request: The chat request containing messages

        Returns:
            ChatResponse with the conversation including the new response
        """
        pass
