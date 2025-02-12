import pytest
from psycopg_pool import AsyncConnectionPool
from convo_history_db.connection import create_db_connection_pool
from unittest.mock import MagicMock

@pytest.mark.asyncio
async def test_create_db_connection_pool():
    settings = MagicMock()
    settings.database.conninfo = "postgresql://user:password@localhost/dbname"
    settings.engine.GROQ_API_KEY = "fake-api-key"
    settings.engine.OPENAI_API_KEY = "fake-api-key"

    pool = create_db_connection_pool(settings)

    assert isinstance(pool, AsyncConnectionPool), "The function should return an instance of AsyncConnectionPool"
    assert not pool._opened, "The connection pool should be closed by default"
    assert pool.conninfo == settings.database.conninfo, "The connection pool should have the correct connection info"
