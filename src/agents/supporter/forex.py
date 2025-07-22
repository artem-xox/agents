import re
from datetime import datetime
from typing import Any, Dict, Optional

from src.agents.base import BaseAgent
from src.domain.entities import ChatRequest, ChatResponse, Message, Role


class ForexClient:
    """
    Mock forex client that provides currency exchange information.
    """

    def __init__(self):
        self.mock_rates = {
            "USD": {
                "EUR": 0.85,
                "GBP": 0.73,
                "JPY": 110.5,
                "CAD": 1.25,
                "AUD": 1.35,
                "CHF": 0.92,
                "CNY": 6.45,
                "RUB": 75.2,
            },
            "EUR": {
                "USD": 1.18,
                "GBP": 0.86,
                "JPY": 130.0,
                "CAD": 1.47,
                "AUD": 1.59,
                "CHF": 1.08,
                "CNY": 7.59,
                "RUB": 88.5,
            },
            "GBP": {
                "USD": 1.37,
                "EUR": 1.16,
                "JPY": 151.4,
                "CAD": 1.71,
                "AUD": 1.85,
                "CHF": 1.26,
                "CNY": 8.82,
                "RUB": 103.0,
            },
            "JPY": {
                "USD": 0.009,
                "EUR": 0.0077,
                "GBP": 0.0066,
                "CAD": 0.0113,
                "AUD": 0.0122,
                "CHF": 0.0083,
                "CNY": 0.058,
                "RUB": 0.68,
            },
        }

        self.currency_names = {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
            "CAD": "Canadian Dollar",
            "AUD": "Australian Dollar",
            "CHF": "Swiss Franc",
            "CNY": "Chinese Yuan",
            "RUB": "Russian Ruble",
        }

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """Get exchange rate between two currencies."""
        from_curr = from_currency.upper()
        to_curr = to_currency.upper()

        # Check if we have direct rate
        if from_curr in self.mock_rates and to_curr in self.mock_rates[from_curr]:
            rate = self.mock_rates[from_curr][to_curr]
        elif to_curr in self.mock_rates and from_curr in self.mock_rates[to_curr]:
            # Calculate inverse rate
            rate = 1 / self.mock_rates[to_curr][from_curr]
        else:
            # Default rate for unknown pairs
            rate = 1.0

        return {
            "from_currency": from_curr,
            "to_currency": to_curr,
            "rate": rate,
            "timestamp": datetime.now().isoformat(),
        }

    def get_currency_info(self, currency: str) -> Dict[str, Any]:
        """Get information about a currency."""
        currency_upper = currency.upper()

        if currency_upper in self.currency_names:
            return {
                "code": currency_upper,
                "name": self.currency_names[currency_upper],
                "available_pairs": list(self.mock_rates.get(currency_upper, {}).keys()),
            }

        return {
            "code": currency_upper,
            "name": "Unknown Currency",
            "available_pairs": [],
        }

    def convert_amount(
        self, amount: float, from_currency: str, to_currency: str
    ) -> Dict[str, Any]:
        """Convert an amount from one currency to another."""
        rate_info = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * rate_info["rate"]

        return {
            "original_amount": amount,
            "original_currency": from_currency.upper(),
            "converted_amount": round(converted_amount, 2),
            "target_currency": to_currency.upper(),
            "exchange_rate": rate_info["rate"],
            "timestamp": rate_info["timestamp"],
        }


class ForexAgent(BaseAgent):
    """
    Forex agent that handles currency exchange queries using function calls.
    """

    NAME = "forex"

    def __init__(self):
        super().__init__()
        self.forex_client = ForexClient()

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
