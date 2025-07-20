import os
from pathlib import Path

from dotenv import load_dotenv

from src.agents.first.agent import OpenAIConfig


def load_env_file(env_file_path: str = ".env") -> None:
    """
    Load environment variables from a .env file using python-dotenv.

    Args:
        env_file_path: Path to the .env file (default: ".env")

    Note:
        This function loads the .env file if it exists. Environment variables
        already set in the system will take precedence over those in the .env file.
    """
    env_path = Path(env_file_path)
    if env_path.exists():
        load_dotenv(env_path, override=False)


# Load .env file when module is imported
load_env_file()


def reload_env_file(env_file_path: str = ".env") -> None:
    """
    Manually reload environment variables from a .env file.
    This can be useful if you want to reload configs during runtime.

    Args:
        env_file_path: Path to the .env file (default: ".env")
    """
    load_env_file(env_file_path)


def get_openai_config() -> OpenAIConfig:
    """
    Initialize OpenAI configuration from environment variables.

    Environment variables:
    - OPENAI_API_KEY: Your OpenAI API key (required)
    - OPENAI_MODEL: Model to use (default: gpt-3.5-turbo)
    - OPENAI_TEMPERATURE: Temperature for generation (default: 0.7)
    - OPENAI_MAX_TOKENS: Maximum tokens for response (default: None)

    Returns:
        OpenAIConfig: Configured OpenAI settings
    """
    return OpenAIConfig(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("OPENAI_MAX_TOKENS"))
        if os.getenv("OPENAI_MAX_TOKENS")
        else None,
    )


def get_streamlit_config() -> dict:
    """
    Initialize Streamlit configuration from environment variables.

    Environment variables:
    - STREAMLIT_PAGE_TITLE: Page title (default: "AI Agents Playground")
    - STREAMLIT_PAGE_ICON: Page icon (default: "🤖")
    - STREAMLIT_LAYOUT: Layout mode (default: "wide")

    Returns:
        dict: Streamlit configuration settings
    """
    return {
        "page_title": os.getenv("STREAMLIT_PAGE_TITLE", "AI Agents Playground"),
        "page_icon": os.getenv("STREAMLIT_PAGE_ICON", "🤖"),
        "layout": os.getenv("STREAMLIT_LAYOUT", "wide"),
    }


def get_app_config() -> dict:
    """
    Initialize general application configuration from environment variables.

    Environment variables:
    - APP_ENV: Environment (development, production, etc.)
    - APP_DEBUG: Debug mode (default: False)
    - APP_LOG_LEVEL: Logging level (default: INFO)

    Returns:
        dict: Application configuration settings
    """
    return {
        "env": os.getenv("APP_ENV", "development"),
        "debug": os.getenv("APP_DEBUG", "false").lower() == "true",
        "log_level": os.getenv("APP_LOG_LEVEL", "INFO"),
    }


# Convenience function to get all configs at once
def get_all_configs() -> dict:
    """
    Get all configuration objects in a single call.

    Returns:
        dict: Dictionary containing all configuration objects
    """
    return {
        "openai": get_openai_config(),
        "streamlit": get_streamlit_config(),
        "app": get_app_config(),
    }
