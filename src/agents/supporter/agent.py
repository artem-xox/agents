import json
from typing import Any, Dict

from src.agents.base import BaseAgent
from src.agents.supporter.forex import ForexAgent
from src.agents.supporter.weather import WeatherAgent
from src.clients.openai import OpenAIClient, OpenAIConfig, OpenAIMessage, OpenAIRequest
from src.domain.entities import ChatRequest, ChatResponse, Message, Role


class SupporterAgent(BaseAgent):
    """
    Personal assistant agent that can help with any question and route to specialized sub-agents using function calling.
    """

    NAME = "orchestrator"

    def __init__(self, openai_config: OpenAIConfig):
        super().__init__()
        self.openai_client = OpenAIClient(openai_config)
        self.weather_agent = WeatherAgent()
        self.forex_agent = ForexAgent()

    def chat(self, request: ChatRequest) -> ChatResponse:
        self.logger.info(
            f"Received supporter request with {len(request.messages)} messages"
        )

        # Use function calling to determine the appropriate action
        return self._process_with_function_calling(request)

    def _process_with_function_calling(self, request: ChatRequest) -> ChatResponse:
        """Process the request using OpenAI function calling for intelligent routing."""

        # Define the functions that can be called
        functions = [
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

        # Convert domain messages to OpenAI format
        openai_messages = []

        # Add system message
        system_message = """You are a helpful personal assistant that can help with any question.
        You have access to specialized functions for weather and forex information.

        CRITICAL RULES:
        1. ANY mention of currency codes (USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, RUB, etc.) → use get_forex
        2. ANY mention of "rate", "convert", "exchange", "currency" → use get_forex
        3. ANY mention of weather, temperature, forecast → use get_weather
        4. For all other questions, respond directly as a helpful assistant.

        Available functions:
        - get_weather: For weather queries (current weather or forecasts)
        - get_forex: For currency conversion and exchange rates (including questions about euros, dollars, pounds, etc.)

        Examples:
        - "100 euros in usd" → use get_forex
        - "convert 50 dollars to euros" → use get_forex
        - "exchange rate for USD to EUR" → use get_forex
        - "rub to eur rate" → use get_forex
        - "usd to gbp" → use get_forex
        - "weather in London" → use get_weather
        - "temperature in Tokyo" → use get_weather

        If the user's query doesn't clearly match weather or forex, respond as a general assistant."""
        openai_messages.append(OpenAIMessage(role=Role.SYSTEM, content=system_message))

        # Add user messages
        for msg in request.messages:
            if msg.role == Role.USER:
                openai_messages.append(OpenAIMessage(role=msg.role, content=msg.text))

        # Create OpenAI request with function calling
        openai_request = OpenAIRequest(
            model=self.openai_client.config.model,
            messages=openai_messages,
            temperature=self.openai_client.config.temperature,
            max_tokens=self.openai_client.config.max_tokens,
            functions=functions,
            function_call="auto",  # Let OpenAI decide when to call functions
        )

        self.logger.info(
            f"Sending request to OpenAI with function calling, model: {openai_request.model}"
        )

        # Get response from OpenAI with function calling
        try:
            openai_response = self.openai_client.chat_completion(openai_request)

            # Check if OpenAI wants to call a function
            if openai_response.function_call:
                last_user_message = (
                    request.messages[-1].text if request.messages else "No message"
                )
                function_name = openai_response.function_call["name"]

                # Fallback check: if it's clearly a forex query but OpenAI called weather, force forex
                if function_name == "get_weather" and self._is_clearly_forex_query(
                    last_user_message
                ):
                    self.logger.warning(
                        f"OpenAI incorrectly called get_weather for forex query: '{last_user_message}', forcing get_forex"
                    )
                    # Create a manual forex function call
                    forex_params = self._extract_forex_params_from_text(
                        last_user_message
                    )
                    if forex_params:
                        manual_function_call = {
                            "name": "get_forex",
                            "arguments": forex_params,
                        }
                        return self._handle_function_call(manual_function_call, request)

                self.logger.info(
                    f"OpenAI requested function call: {function_name} for user query: '{last_user_message}'"
                )
                return self._handle_function_call(
                    openai_response.function_call, request
                )
            else:
                # Regular response
                assistant_message = Message(
                    role=Role.ASSISTANT, text=openai_response.content, agent=self.NAME
                )
                self.logger.info("Generated assistant response")
                return ChatResponse(messages=request.messages + [assistant_message])

        except Exception as e:
            self.logger.error(f"Error getting response from OpenAI: {e}")
            raise

    def _is_clearly_forex_query(self, text: str) -> bool:
        """Check if the text is clearly a forex query."""
        text_lower = text.lower()

        # Currency codes
        currency_codes = ["usd", "eur", "gbp", "jpy", "cad", "aud", "chf", "cny", "rub"]
        has_currency = any(code in text_lower for code in currency_codes)

        # Forex keywords
        forex_keywords = [
            "rate",
            "convert",
            "exchange",
            "currency",
            "dollar",
            "euro",
            "pound",
            "yen",
            "franc",
            "yuan",
            "ruble",
        ]
        has_forex_keywords = any(keyword in text_lower for keyword in forex_keywords)

        return has_currency or has_forex_keywords

    def _extract_forex_params_from_text(self, text: str) -> Dict[str, Any]:
        """Extract forex parameters from text as fallback."""
        import re

        text_lower = text.lower()

        # Currency patterns
        currency_patterns = {
            "usd": "USD",
            "dollar": "USD",
            "dollars": "USD",
            "eur": "EUR",
            "euro": "EUR",
            "euros": "EUR",
            "gbp": "GBP",
            "pound": "GBP",
            "pounds": "GBP",
            "jpy": "JPY",
            "yen": "JPY",
            "cad": "CAD",
            "canadian": "CAD",
            "aud": "AUD",
            "australian": "AUD",
            "chf": "CHF",
            "franc": "CHF",
            "swiss": "CHF",
            "cny": "CNY",
            "yuan": "CNY",
            "chinese": "CNY",
            "rub": "RUB",
            "ruble": "RUB",
            "russian": "RUB",
        }

        # Extract currencies
        currencies = []
        for pattern, code in currency_patterns.items():
            if pattern in text_lower and code not in currencies:
                currencies.append(code)

        if len(currencies) >= 2:
            # Extract amount
            numbers = re.findall(r"\d+(?:\.\d+)?", text)
            amount = float(numbers[0]) if numbers else None

            # Determine action
            action = "convert" if "convert" in text_lower or amount else "rate"

            return {
                "action": action,
                "from_currency": currencies[0],
                "to_currency": currencies[1],
                "amount": amount,
            }

        return {}

    def _handle_function_call(
        self, function_call: Dict[str, Any], request: ChatRequest
    ) -> ChatResponse:
        """Handle the detected function call."""
        function_name = function_call["name"]
        parameters = function_call["arguments"]

        # Parse the arguments if they're a string
        if isinstance(parameters, str):
            try:
                parameters = json.loads(parameters)
            except json.JSONDecodeError:
                self.logger.error(f"Failed to parse function arguments: {parameters}")
                return self._process_general_question(request)

        self.logger.info(
            f"Handling function call: {function_name} with parameters: {parameters}"
        )

        if function_name == "get_weather":
            return self._handle_weather_function(parameters, request)
        elif function_name == "get_forex":
            return self._handle_forex_function(parameters, request)
        else:
            # Fallback to general response
            return self._process_general_question(request)

    def _handle_weather_function(
        self, parameters: Dict[str, Any], request: ChatRequest
    ) -> ChatResponse:
        """Handle weather function call."""
        location = parameters.get("location", "new york")
        query_type = parameters.get("query_type", "current")

        # Create a request with the extracted parameters
        weather_query = f"What's the {query_type} weather in {location}?"
        weather_message = Message(role=Role.USER, text=weather_query, agent=self.NAME)
        weather_request = ChatRequest(messages=[weather_message])

        self.logger.info(f"Calling WeatherAgent for {query_type} weather in {location}")
        sub_response = self.weather_agent.chat(weather_request)

        # Return the full conversation context with the assistant's response
        return ChatResponse(messages=request.messages + [sub_response.messages[-1]])

    def _handle_forex_function(
        self, parameters: Dict[str, Any], request: ChatRequest
    ) -> ChatResponse:
        """Handle forex function call."""
        action = parameters.get("action", "rate")
        from_currency = parameters.get("from_currency", "USD")
        to_currency = parameters.get("to_currency", "EUR")
        amount = parameters.get("amount")

        if action == "convert" and amount:
            forex_query = f"Convert {amount} {from_currency} to {to_currency}"
        else:
            forex_query = f"What's the {from_currency} to {to_currency} rate?"

        forex_message = Message(role=Role.USER, text=forex_query, agent=self.NAME)
        forex_request = ChatRequest(messages=[forex_message])

        self.logger.info(
            f"Calling ForexAgent for {action}: {from_currency} to {to_currency}"
        )
        sub_response = self.forex_agent.chat(forex_request)

        # Return the full conversation context with the assistant's response
        return ChatResponse(messages=request.messages + [sub_response.messages[-1]])

    def _process_general_question(self, request: ChatRequest) -> ChatResponse:
        """Process general questions using the main assistant."""
        # Convert domain messages to OpenAI format
        openai_messages = []

        # Add system message
        system_message = """You are a helpful personal assistant that can help with any question.
        You can provide information, answer questions, and help with various tasks.
        Be friendly, informative, and helpful in your responses."""
        openai_messages.append(OpenAIMessage(role=Role.SYSTEM, content=system_message))

        # Add user messages
        for msg in request.messages:
            if msg.role == Role.USER:
                openai_messages.append(OpenAIMessage(role=msg.role, content=msg.text))

        # Create OpenAI request
        openai_request = OpenAIRequest(
            model=self.openai_client.config.model,
            messages=openai_messages,
            temperature=self.openai_client.config.temperature,
            max_tokens=self.openai_client.config.max_tokens,
        )

        self.logger.info(
            f"Sending general question to OpenAI with model: {openai_request.model}"
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
        assistant_message = Message(
            role=Role.ASSISTANT, text=openai_response.content, agent=self.NAME
        )

        self.logger.info("Generated assistant response")
        return ChatResponse(messages=request.messages + [assistant_message])
