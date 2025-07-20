# Supporter Agent

The Supporter agent is a personal assistant that can help with any question and automatically routes specialized queries to appropriate sub-agents.

## Architecture

```
SupporterAgent
├── WeatherAgent (for weather queries)
└── ForexAgent (for currency/forex queries)
```

## Features

### Main Supporter Agent
- Acts as a general personal assistant
- Automatically routes queries to specialized sub-agents
- Handles general questions using OpenAI
- Provides friendly and helpful responses

### WeatherAgent
- Provides current weather information
- Offers 5-day weather forecasts
- Supports multiple cities (New York, London, Tokyo, Sydney)
- Returns formatted weather data with emojis

**Supported queries:**
- "What's the weather like in [city]?"
- "What's the forecast for [city]?"
- "How's the weather in [city]?"

### ForexAgent
- Currency conversion between major currencies
- Real-time exchange rates
- Supports 8 major currencies (USD, EUR, GBP, JPY, CAD, AUD, CHF, CNY, RUB)

**Supported queries:**
- "Convert 100 USD to EUR"
- "What's the USD to GBP rate?"
- "How much is 50 EUR in USD?"

## Usage

### In the UI
1. Select "Supporter" from the agent dropdown
2. Ask any question - OpenAI will intelligently route to the appropriate sub-agent
3. **Weather examples**:
   - "What's the weather like in Tokyo?"
   - "Show me the forecast for London"
   - "How hot is it in Sydney?"
4. **Forex examples**:
   - "Convert 100 USD to EUR"
   - "What's the exchange rate for USD to GBP?"
   - "How much is 50 euros in dollars?"
5. **General questions**: Ask anything else

### Programmatically
```python
from src.agents.supporter.agent import SupporterAgent
from src.clients.openai import OpenAIConfig
from src.domain.entities import ChatRequest, Message, Role

# Initialize the agent
config = OpenAIConfig(api_key="your-api-key")
agent = SupporterAgent(config)

# Ask a question - OpenAI will automatically detect intent and call appropriate function
request = ChatRequest(messages=[
    Message(role=Role.USER, text="What's the weather in Tokyo?")
])
response = agent.chat(request)
print(response.messages[-1].text)
```

### Function Calling Examples

The agent automatically calls functions based on user intent:

```python
# Weather function call
"Show me the weather in Paris"
→ get_weather(location="paris", query_type="current")

# Forex function call
"Convert 200 dollars to euros"
→ get_forex(action="convert", from_currency="USD", to_currency="EUR", amount=200)

# Exchange rate function call
"What's the USD to JPY rate?"
→ get_forex(action="rate", from_currency="USD", to_currency="JPY")
```

## Mock Data

Both WeatherAgent and ForexAgent use mock data for demonstration purposes:

### Weather Data
- **New York**: 22°C, partly cloudy, 65% humidity
- **London**: 15°C, rainy, 80% humidity
- **Tokyo**: 28°C, sunny, 70% humidity
- **Sydney**: 25°C, sunny, 60% humidity

### Forex Data
- USD/EUR: 0.85
- USD/GBP: 0.73
- USD/JPY: 110.5
- And more currency pairs...

## Function Calling Architecture

The SupporterAgent uses OpenAI's function calling for intelligent routing:

### Available Functions

1. **`get_weather`**: Handles weather queries
   - Parameters: `location` (required), `query_type` (current/forecast)
   - Example: "What's the weather in Tokyo?" → calls `get_weather(location="tokyo", query_type="current")`

2. **`get_forex`**: Handles currency exchange queries
   - Parameters: `action` (convert/rate), `from_currency`, `to_currency`, `amount` (optional)
   - Example: "Convert 100 USD to EUR" → calls `get_forex(action="convert", from_currency="USD", to_currency="EUR", amount=100)`

### Intelligent Routing

- **OpenAI decides** when to call functions based on user intent
- **No keyword matching** - uses natural language understanding
- **Parameter extraction** is handled automatically by OpenAI
- **Fallback to general assistant** for non-specialized queries

### Context Optimization

For efficiency and cost savings:
- **Sub-agents (Weather/Forex)**: Only receive the last user message, not the full conversation context
- **General queries**: Receive the full conversation context for better continuity
- **Response handling**: Sub-agent responses are properly integrated back into the full conversation flow

**Benefits:**
- **Intelligent routing** using OpenAI's natural language understanding
- **Automatic parameter extraction** from user queries
- **Reduced token usage** for specialized queries
- **Faster response times** for weather and forex requests
- **Lower API costs** when using external services
- **Maintains conversation flow** while optimizing performance

## Extending

To add new sub-agents:

1. Create a new agent class inheriting from `BaseAgent`
2. Add routing logic in `SupporterAgent._is_[type]_query()`
3. Initialize the new agent in `SupporterAgent.__init__()`
4. Add routing in `SupporterAgent.chat()`

## Dependencies

- OpenAI API for general questions
- Mock clients for weather and forex data
- Standard Python libraries (datetime, typing, etc.)
