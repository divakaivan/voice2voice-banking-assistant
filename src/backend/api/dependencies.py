from typing import AsyncIterator, cast
from uuid import uuid4

from fastapi import WebSocket
from groq import AsyncGroq
from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool
from pydantic import UUID4
from pydantic_ai import Agent

from backend.config.settings import get_settings
from backend.customer_transaction_db.connection import get_customer_sqlite_client
from backend.nlp_processor.text_to_speech import TextToSpeech
from backend.ai_services.agent import Dependencies


async def get_db_conn(websocket: WebSocket) -> AsyncIterator[AsyncConnection]:
    """
    Gets a connection to the database using the connection pool.

    Args:
        websocket: WebSocket connection.

    Yields:
        Connection to the database.
    """
    db_pool = cast(AsyncConnectionPool, websocket.state.pool)
    async with db_pool.connection() as conn:
        yield conn


async def get_conversation_id() -> UUID4:
    """
    Creates a new unique conversation ID.

    Returns:
        Conversation ID.
    """
    return uuid4()


async def get_agent_dependencies() -> Dependencies:
    """
    Gets the dependencies for the PydanticAI Agent.

    Returns:
        Dependencies instance.
    """
    return Dependencies(
        settings=get_settings(),
        sqlite_db=get_customer_sqlite_client(),
    )


async def get_groq_client(websocket: WebSocket) -> AsyncGroq:
    """
    Gets a client for interacting with Groq API.

    Args:
        websocket: WebSocket connection.

    Returns:
        Client for interacting with Groq API
    """
    return websocket.state.groq_client


async def get_agent(websocket: WebSocket) -> Agent:
    """
    Gets a PydanticAI Agent that uses Groq models.

    Args:
        websocket: WebSocket connection.

    Returns:
        PydanticAI Agent that uses Groq models.
    """
    return websocket.state.groq_agent


async def get_tts_handler(websocket: WebSocket) -> TextToSpeech:
    """
    Gets a handler for text-to-speech conversion.

    Args:
        websocket: WebSocket connection.

    Returns:
        Handler for text-to-speech conversion.
    """
    return TextToSpeech(
        client=websocket.state.openai_client,
        model_name="tts-1",
        response_format="aac",
    )
