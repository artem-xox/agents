# AI Agents Playground

A personal playground for experimenting with AI agents, featuring a modern web UI built with Streamlit.

## Overview

This project is my personal sandbox for developing and testing various AI agent implementations. It provides a clean, modular architecture for building different types of agents and a user-friendly interface to interact with them.

## Features

- **Modular Agent Architecture**: Clean separation between agent implementations and the domain layer
- **Web UI**: Interactive Streamlit-based interface for chatting with agents
- **Multiple Agent Types**: Support for different agent implementations (Dummy, OpenAI-based, etc.)
- **Type Safety**: Full type hints and modern Python practices
- **Easy Configuration**: Environment-based configuration for API keys and settings

## Project Structure

```
src/
├── agents/           # Agent implementations
│   ├── dummy/       # Simple echo agent for testing
│   └── first/       # OpenAI-powered agent
├── domain/          # Core domain entities and interfaces
├── ui/              # Streamlit web interface
│   ├── pages/       # Different UI pages
│   └── main.py      # Main UI entry point
```

## Getting Started

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd agents
```

2. Install dependencies:
```bash
make install
```

3. Set up your OpenAI API key (optional, for OpenAI-based agents):
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Running the Application

Start the web UI:
```bash
make ui
```

This will launch the Streamlit interface at `http://localhost:8501`.

## Available Agents

### Dummy Agent
A simple echo agent that repeats your messages. Perfect for testing the interface without API costs.

### First Agent (OpenAI)
A GPT-powered agent using OpenAI's API. Requires an OpenAI API key to function.

## Development

### Adding New Agents

1. Create a new directory in `src/agents/`
2. Implement the `Agent` interface from `src/domain/agent.py`
3. Add your agent to the UI mapping in `src/ui/pages/1_dialog.py`

### Code Quality

The project uses modern Python tooling:

- **Ruff**: Fast Python linter and formatter
- **Black**: Code formatting
- **isort**: Import sorting
- **Type hints**: Full type safety

Run linting:
```bash
make lint
```

## Architecture

The project follows a clean architecture pattern:

- **Domain Layer**: Core entities (`Message`, `ChatRequest`, `ChatResponse`) and interfaces (`Agent`)
- **Agent Layer**: Concrete implementations of different AI agents
- **UI Layer**: Streamlit-based web interface for user interaction

This separation makes it easy to add new agent types or modify the UI without affecting the core domain logic.

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## Contributing

This is a personal playground project, but feel free to fork and experiment with your own agent implementations!
