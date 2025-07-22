import re
from typing import Optional

from src.agents.base import BaseAgent
from src.agents.supporter.forex.mocks import ForexClient
from src.agents.supporter.forex.prompt import SYSTEM_PROMPT
from src.agents.supporter.forex.tools import FUNCTIONS
from src.clients.openai import OpenAIClient
from src.domain.entities import ChatRequest, ChatResponse, Message, Role


class ForexAgent(BaseAgent):
    """
    Forex agent that handles currency exchange queries using function calls.
    """

    NAME = "forex"

    def __init__(self, openai_client: OpenAIClient):
        super().__init__()
        self.forex_client = ForexClient()
        self.openai_client = openai_client
        self.functions = FUNCTIONS
        self.system_prompt = SYSTEM_PROMPT

    def chat(self, request: ChatRequest) -> ChatResponse:
        self.logger.info(
            f"Received forex request with {len(request.messages)} messages (context optimized)"
        )

        # Get the last user message
        last_message = request.messages[-1].text

        # Determine the type of forex query
        if "convert" in last_message.lower() or any(
            char.isdigit() for char in last_message
        ):
            response_text = self._handle_conversion_query(last_message)
        elif "rate" in last_message.lower():
            response_text = self._handle_rate_query(last_message)
        else:
            response_text = self._handle_general_forex_query(last_message)

        # Create assistant message
        assistant_message = Message(
            role=Role.ASSISTANT, text=response_text, agent=self.NAME
        )

        self.logger.info("Generated forex response")
        return ChatResponse(messages=request.messages + [assistant_message])

    def _handle_conversion_query(self, message: str) -> str:
        """Handle currency conversion queries."""
        # Extract amount and currencies (simplified extraction)
        amount = self._extract_amount(message)
        currencies = self._extract_currencies(message)

        if len(currencies) >= 2 and amount:
            from_currency, to_currency = currencies[0], currencies[1]
            conversion = self.forex_client.convert_amount(
                amount, from_currency, to_currency
            )

            return f"""💱 Currency Conversion:

💰 {conversion["original_amount"]} {conversion["original_currency"]} = {conversion["converted_amount"]} {conversion["target_currency"]}

📊 Exchange Rate: 1 {conversion["original_currency"]} = {conversion["exchange_rate"]} {conversion["target_currency"]}

⏰ Last Updated: {conversion["timestamp"]}

This is mock data for demonstration purposes."""
        else:
            return "I couldn't understand the conversion request. Please specify an amount and two currencies (e.g., 'convert 100 USD to EUR')."

    def _handle_rate_query(self, message: str) -> str:
        """Handle exchange rate queries."""
        currencies = self._extract_currencies(message)

        if len(currencies) >= 2:
            from_currency, to_currency = currencies[0], currencies[1]
            rate_info = self.forex_client.get_exchange_rate(from_currency, to_currency)

            return f"""📈 Exchange Rate:

💱 {rate_info["from_currency"]} to {rate_info["to_currency"]}: {rate_info["rate"]}

⏰ Last Updated: {rate_info["timestamp"]}

This is mock data for demonstration purposes."""
        else:
            return "Please specify two currencies to get the exchange rate (e.g., 'USD to EUR rate')."

    def _handle_general_forex_query(self, message: str) -> str:
        """Handle general forex queries."""
        return """💱 Forex Information:

I can help you with:
• Currency conversion (e.g., "convert 100 USD to EUR")
• Exchange rates (e.g., "USD to EUR rate")
• Currency information

Available currencies: USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, RUB

This is mock data for demonstration purposes."""

    def _extract_amount(self, message: str) -> Optional[float]:
        """Extract amount from message."""
        numbers = re.findall(r"\d+(?:\.\d+)?", message)
        if numbers:
            return float(numbers[0])
        return None

    def _extract_currencies(self, message: str) -> list[str]:
        """Extract currency codes from message."""
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

        message_lower = message.lower()
        currencies = []

        for pattern, code in currency_patterns.items():
            if pattern in message_lower and code not in currencies:
                currencies.append(code)

        return currencies
