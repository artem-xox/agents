from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.supporter.weather.mocks import WeatherClient
from src.agents.supporter.weather.prompt import SYSTEM_PROMPT
from src.agents.supporter.weather.tools import FUNCTIONS
from src.clients.openai import OpenAIClient
from src.domain.entities import ChatRequest, ChatResponse, Message, Role


class WeatherAgent(BaseAgent):
    """
    Weather agent that handles weather-related queries using function calls.
    """

    NAME = "weather"

    def __init__(self, openai_client: OpenAIClient):
        super().__init__()
        self.weather_client = WeatherClient()
        self.openai_client = openai_client
        self.functions = FUNCTIONS
        self.system_prompt = SYSTEM_PROMPT

    def chat(self, request: ChatRequest) -> ChatResponse:
        self.logger.info(
            f"Received weather request with {len(request.messages)} messages (context optimized)"
        )

        # Get the last user message
        last_message = request.messages[-1].text

        # Extract location and type of weather info needed
        location = self._extract_location(last_message)
        is_forecast = "forecast" in last_message.lower()

        if is_forecast:
            weather_data = self.weather_client.get_forecast(location)
            response_text = self._format_forecast_response(weather_data)
        else:
            weather_data = self.weather_client.get_current_weather(location)
            response_text = self._format_current_weather_response(weather_data)

        # Create assistant message
        assistant_message = Message(
            role=Role.ASSISTANT, text=response_text, agent=self.NAME
        )

        self.logger.info("Generated weather response")
        return ChatResponse(messages=request.messages + [assistant_message])

    def _extract_location(self, message: str) -> str:
        """Extract location from the message."""
        # Simple location extraction - in a real implementation, you might use NLP
        common_cities = [
            "new york",
            "london",
            "tokyo",
            "sydney",
            "paris",
            "berlin",
            "moscow",
        ]

        message_lower = message.lower()
        for city in common_cities:
            if city in message_lower:
                return city

        # Default to a common city if no specific location found
        return "new york"

    def _format_current_weather_response(self, weather_data: Dict[str, Any]) -> str:
        """Format current weather data into a readable response."""
        return f"""🌤️ Current Weather for {weather_data["location"]}:

🌡️ Temperature: {weather_data["temperature"]}°C
☁️ Condition: {weather_data["condition"].title()}
💧 Humidity: {weather_data["humidity"]}%
💨 Wind Speed: {weather_data["wind_speed"]} km/h

This is mock data for demonstration purposes."""

    def _format_forecast_response(self, weather_data: Dict[str, Any]) -> str:
        """Format forecast data into a readable response."""
        forecast_text = "\n".join(
            [f"  • {day.title()}" for day in weather_data["forecast"]]
        )

        return f"""📅 5-Day Forecast for {weather_data["location"]}:

{forecast_text}

This is mock data for demonstration purposes."""
