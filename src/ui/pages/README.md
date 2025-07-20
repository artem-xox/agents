# UI Pages Configuration

This directory contains the Streamlit UI pages and centralized configuration management.

## Configuration System

The `configs.py` file provides centralized configuration management using environment variables. This allows for easy customization without modifying code.

### Available Environment Variables

#### OpenAI Configuration
- `OPENAI_API_KEY`: Your OpenAI API key (required for OpenAI-based agents)
- `OPENAI_MODEL`: Model to use (default: `gpt-3.5-turbo`)
- `OPENAI_TEMPERATURE`: Temperature for generation (default: `0.7`)
- `OPENAI_MAX_TOKENS`: Maximum tokens for response (default: `None`)

#### Streamlit Configuration
- `STREAMLIT_PAGE_TITLE`: Page title (default: `AI Agents Playground`)
- `STREAMLIT_PAGE_ICON`: Page icon (default: `🤖`)
- `STREAMLIT_LAYOUT`: Layout mode (default: `wide`)

#### Application Configuration
- `APP_ENV`: Environment (development, production, etc.) (default: `development`)
- `APP_DEBUG`: Debug mode (default: `false`)
- `APP_LOG_LEVEL`: Logging level (default: `INFO`)

### Usage Example

Create a `.env` file in your project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7

# Streamlit Configuration
STREAMLIT_PAGE_TITLE=My AI Agents
STREAMLIT_PAGE_ICON=🚀
STREAMLIT_LAYOUT=wide

# Application Configuration
APP_ENV=development
APP_DEBUG=true
APP_LOG_LEVEL=DEBUG
```

**Note**: The `.env` file is automatically loaded when the `configs` module is imported using python-dotenv. Environment variables already set in your system will take precedence over those in the `.env` file.

### Using Configurations in Code

```python
from src.ui.pages.configs import get_openai_config, get_streamlit_config, get_all_configs, reload_env_file

# Get specific configuration
openai_config = get_openai_config()
streamlit_config = get_streamlit_config()

# Or get all configurations at once
all_configs = get_all_configs()

# Manually reload .env file if needed
reload_env_file()
```

## Pages

- `1_dialog.py`: Main chat interface for interacting with agents
- `2_assessment.py`: Assessment interface (placeholder)
- `configs.py`: Centralized configuration management
