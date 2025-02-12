from contextlib import asynccontextmanager
from typing import AsyncIterator, TypedDict

from fastapi import FastAPI
from groq import AsyncGroq
from loguru import logger
from openai import AsyncOpenAI
from psycopg_pool import AsyncConnectionPool
from pydantic_ai import Agent, Tool


from backend.config.settings import get_settings
from backend.convo_history_db.actions import create_main_table
from backend.convo_history_db.connection import create_db_connection_pool
from backend.ai_services.agent import Dependencies, create_groq_agent
from backend.ai_services.factories import (
    create_groq_client,
    create_groq_model,
    create_openai_client,
)
from backend.ai_services.tools import (
    get_recent_transactions,
    summarize_spending,
    detect_unusual_spending,
)


class State(TypedDict):
    """Application state container for shared resources.

    Attributes:
        pool: Conversation history database connection pool for async operations.
        groq_client: Client for interacting with Groq API.
        openai_client: Client for interacting with OpenAI API.
        groq_agent: PydanticAI Agent that uses Groq models.
    """

    pool: AsyncConnectionPool
    groq_client: AsyncGroq
    openai_client: AsyncOpenAI
    groq_agent: Agent[Dependencies]


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[State]:
    """Manages application lifecycle and shared resources.

    Handles initialization and cleanup of application-wide resources
    during startup and shutdown phases.

    Args:
        app: FastAPI application instance.

    Yields:
        Application state containing shared resources.
    """
    settings = get_settings()
    pool = create_db_connection_pool(settings=settings)
    openai_client = create_openai_client(settings=settings)
    groq_client = create_groq_client(settings=settings)
    _groq_model = create_groq_model(groq_client=groq_client)
    groq_agent = create_groq_agent(
        groq_model=_groq_model,
        tools=[
            Tool(
                function=get_recent_transactions, 
                takes_ctx=True, 
            ),
            Tool(
                function=summarize_spending, 
                takes_ctx=True,
            ),
            Tool(
                function=detect_unusual_spending, 
                takes_ctx=True, 
            ),
        ],
        system_prompt = """
            You are a helpful and polite bank assistant, dedicated to providing concise and clear information about the user's bank transactions.
            You will interact with the user in a friendly and professional manner. 
            When the user inquires about their transactions, summarize the details clearly and briefly, highlighting key information like amounts, dates, and merchants.
            If you’re given a date (e.g., 01-01-2023, 14-10-2023), make sure to format it in a human-friendly way, like '1st of January 2023' and '14th of October 2023' to make it easier to read and understand.

            You can also offer insights like budgeting information, recent spending patterns, and help with transaction analysis.
            You have access to the following tools:\n\n
            - **get_recent_transactions**: Retrieve the most recent transactions based on filters such as start and end date, category, and merchant.\n
            - **summarize_spending**: Summarize spending for a given time period, such as 'this week' or 'last month', and optionally include budget status.\n
            - **detect_unusual_spending**: Identify transactions that deviate from usual spending behavior based on a specified threshold and time period.\n
            These tools allow you to help answer user queries.
            If the user just says 'Hello', 'Hi', 'Thank you', or 'Bye', you can respond with a friendly greeting and say 'I am here to help you with your banking.'
        """

    )

    logger.info("Opening database connection pool")
    await pool.open()
    await create_main_table(pool)

    yield {
        "pool": pool,
        "openai_client": openai_client,
        "groq_client": groq_client,
        "groq_agent": groq_agent,
    }

    logger.info("Closing database connection pool")
    await pool.close()

    logger.info("Closing OpenAI client")
    await openai_client.close()

    logger.info("Closing Groq client")
    await groq_client.close()
