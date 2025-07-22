FUNCTIONS = [
    {
        "name": "get_weather",
        "description": "Get current weather information or forecast for a specific location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city or location to get weather for",
                },
                "query_type": {
                    "type": "string",
                    "enum": ["current", "forecast"],
                    "description": "Whether to get current weather or forecast",
                },
            },
            "required": ["location"],
        },
    },
    {
        "name": "get_forex",
        "description": "Get currency exchange rates or convert between currencies. Use this for ANY currency-related queries including USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, RUB, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["convert", "rate"],
                    "description": "Whether to convert currency or get exchange rate",
                },
                "from_currency": {
                    "type": "string",
                    "description": "Source currency code (USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, RUB, etc.)",
                },
                "to_currency": {
                    "type": "string",
                    "description": "Target currency code (USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, RUB, etc.)",
                },
                "amount": {
                    "type": "number",
                    "description": "Amount to convert (required for conversion)",
                },
            },
            "required": ["action", "from_currency", "to_currency"],
        },
    },
]
