# AI Agents Playground

A personal playground for experimenting with AI agents, featuring a modern web UI built with Streamlit and local dialog persistence.

## Overview

This project is my personal sandbox for developing and testing various AI agent implementations. It provides a clean, modular architecture for building different types of agents and a user-friendly interface to interact with them. The application includes a local dialog cache system that automatically saves and manages conversation history.

## Features

- **Modular Agent Architecture**: Clean separation between agent implementations and the domain layer
- **Web UI**: Interactive Streamlit-based interface for chatting with agents
- **Local Dialog Cache**: Automatic saving and management of conversation history in JSON format
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
├── infra/           # Infrastructure components
│   └── cache/       # Dialog cache implementation
├── ui/              # Streamlit web interface
│   ├── pages/       # Different UI pages
│   └── main.py      # Main UI entry point
dialog_cache/         # Local storage for saved dialogs (auto-created)
```

## Dialog Cache System

The application includes a robust local dialog cache system that automatically manages your conversation history:

### Features

- **Automatic Saving**: Every conversation is automatically saved after each message exchange
- **Local Storage**: All dialogs are stored locally in JSON format in the `dialog_cache/` directory
- **Easy Management**: Load, delete, and start new conversations through the web interface
- **Persistent History**: Conversations survive application restarts
- **Metadata Tracking**: Each dialog includes creation date, message count, and unique ID

### Usage

#### Starting a New Dialog
- Click the "Start a new dialog" button in the sidebar
- The current conversation will be automatically saved before starting fresh

#### Loading Previous Dialogs
- Use the "Load Previous Dialog" dropdown in the sidebar
- Select any saved conversation to load it instantly
- Dialogs are sorted by creation date (newest first)

#### Managing Dialogs
- View current dialog information in the sidebar
- Delete unwanted conversations using the delete dialog section
- All operations are performed locally - no data is sent to external servers

### Technical Details

#### Storage Format
Dialogs are saved as JSON files with the following structure:
```json
{
  "dialog_id": "20241201_143022",
  "created_at": "2024-12-01T14:30:22.123456",
  "messages": [
    {
      "role": "user",
      "text": "Hello, how are you?"
    },
    {
      "role": "assistant",
      "text": "I'm doing well, thank you for asking!"
    }
  ]
}
```

#### File Organization
- **Location**: `dialog_cache/` directory (auto-created)
- **Naming**: Files use timestamp-based IDs (YYYYMMDD_HHMMSS format)
- **Git Ignored**: The cache directory is excluded from version control

#### Cache Management
The `DialogCache` class provides these operations:
- `save_dialog()`: Save conversation to local storage
- `load_dialog()`: Load conversation from storage
- `list_dialogs()`: Get all available dialogs with metadata
- `delete_dialog()`: Remove dialog from storage
- `get_dialog_info()`: Get dialog metadata without loading messages

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
- **Infrastructure Layer**: Dialog cache and other infrastructure components
- **UI Layer**: Streamlit-based web interface for user interaction

This separation makes it easy to add new agent types or modify the UI without affecting the core domain logic.

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## Contributing

This is a personal playground project, but feel free to fork and experiment with your own agent implementations!
