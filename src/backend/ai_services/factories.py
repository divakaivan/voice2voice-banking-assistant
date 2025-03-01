from groq import AsyncGroq
from openai import AsyncOpenAI
from pydantic_ai.models.groq import GroqModel

from config.settings import Settings

def create_groq_client(
    settings: Settings,
) -> AsyncGroq:
    """
    Creates a client for interacting with Groq API.

    Args:
        settings: Application settings.

    Returns:
        Client for interacting with Groq API
    """
    return AsyncGroq(api_key=settings.engine.GROQ_API_KEY)


def create_openai_client(
    settings: Settings,
) -> AsyncOpenAI:
    """
    Creates a client for interacting with OpenAI API.

    Args:
        settings: Application settings.

    Returns:
        Client for interacting with OpenAI API
    """
    return AsyncOpenAI(api_key=settings.engine.OPENAI_API_KEY)


def create_groq_model(
    groq_client: AsyncGroq,
) -> GroqModel:
    """
    Creates a Groq model for PydanticAI.

    Args:
        groq_client: Client for interacting with Groq API.

    Returns:
        Groq model for PydanticAI
    """
    return GroqModel(
        model_name="llama-3.3-70b-versatile",
        groq_client=groq_client,
    )
