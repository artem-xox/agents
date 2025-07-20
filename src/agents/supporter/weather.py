from typing import Any, Dict

from src.agents.base import BaseAgent
from src.domain.entities import ChatRequest, ChatResponse, Message, Role


class WeatherClient:
    """
    Mock weather client that provides weather information.
    """

    def __init__(self):
        self.mock_data = {
            "new york": {
                "temperature": 22,
                "condition": "partly cloudy",
                "humidity": 65,
                "wind_speed": 12,
                "forecast": ["sunny", "cloudy", "rain", "sunny", "partly cloudy"],
            },
            "london": {
                "temperature": 15,
                "condition": "rainy",
                "humidity": 80,
                "wind_speed": 18,
                "forecast": ["rainy", "cloudy", "sunny", "rainy", "cloudy"],
            },
            "tokyo": {
                "temperature": 28,
                "condition": "sunny",
                "humidity": 70,
                "wind_speed": 8,
                "forecast": ["sunny", "sunny", "cloudy", "rain", "sunny"],
            },
            "sydney": {
                "temperature": 25,
                "condition": "sunny",
                "humidity": 60,
                "wind_speed": 15,
                "forecast": ["sunny", "partly cloudy", "sunny", "cloudy", "sunny"],
            },
        }

    def get_current_weather(self, location: str) -> Dict[str, Any]:
        """Get current weather for a location."""
        location_lower = location.lower()

        # Try to find exact match or partial match
        for city, data in self.mock_data.items():
            if location_lower in city or city in location_lower:
                return {
                    "location": city.title(),
                    "temperature": data["temperature"],
                    "condition": data["condition"],
                    "humidity": data["humidity"],
                    "wind_speed": data["wind_speed"],
                }

        # Default response for unknown locations
        return {
            "location": location.title(),
            "temperature": 20,
            "condition": "unknown",
            "humidity": 50,
            "wind_speed": 10,
        }

    def get_forecast(self, location: str, days: int = 5) -> Dict[str, Any]:
        """Get weather forecast for a location."""
        location_lower = location.lower()

        for city, data in self.mock_data.items():
            if location_lower in city or city in location_lower:
                return {"location": city.title(), "forecast": data["forecast"][:days]}

        return {"location": location.title(), "forecast": ["unknown"] * days}


class WeatherAgent(BaseAgent):
    """
    Weather agent that handles weather-related queries using function calls.
    """

    def __init__(self):
        super().__init__()
        self.weather_client = WeatherClient()

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
        assistant_message = Message(role=Role.ASSISTANT, text=response_text)

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
