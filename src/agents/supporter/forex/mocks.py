from datetime import datetime
from typing import Any, Dict


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
