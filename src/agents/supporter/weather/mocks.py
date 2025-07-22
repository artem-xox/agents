from typing import Any, Dict


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
