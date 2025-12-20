import os
from dotenv import load_dotenv
from typing import Dict


def load_env_variables():
    """
    Loads environment variables from a .env file.
    """
    load_dotenv()

def get_env_variable(key: str, default: str = None) -> str:
    """
    Retrieves an environment variable.
    Raises an error if the variable is not found and no default is provided.
    """
    value = os.getenv(key)
    if value is None and default is None:
        raise ValueError(f"Environment variable '{key}' not set.")
    return value if value is not None else default

async def check_qdrant_status() -> str:
    """
    Checks the connectivity status of Qdrant.
    """
    try:
        # Lazy import to avoid circular dependencies during initialization
        from backend.retrieval import qdrant_client
        health_info = await qdrant_client.get_collection_info(collection_name="any_collection_name") # Attempt to connect
        # If no exception, it means the client is connected, even if collection doesn't exist
        return "connected"
    except Exception as e:
        return f"disconnected: {e}"

async def check_cohere_status() -> str:
    """
    Checks the connectivity status of Cohere.
    """
    try:
        from backend.retrieval import cohere_client
        # Perform a small embedding call to check connectivity
        cohere_client.embed(texts=["test"], model="embed-english-light-v3.0", input_type="search_query")
        return "connected"
    except Exception as e:
        return f"disconnected: {e}"

async def check_gemini_status() -> str:
    """
    Checks the connectivity status of Gemini.
    """
    try:
        import google.generativeai as genai
        # Attempt a simple API call, e.g., list models, to check connectivity
        # This will raise an exception if the API key is invalid or connection fails
        genai.list_models()
        return "connected"
    except Exception as e:
        return f"disconnected: {e}"
