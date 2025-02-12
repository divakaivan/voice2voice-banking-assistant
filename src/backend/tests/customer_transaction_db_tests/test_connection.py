import pytest
import aiosqlite
from customer_transaction_db.connection import get_customer_sqlite_client

@pytest.mark.asyncio
async def test_get_customer_sqlite_client():
    async def get_db_connection():
        async for db in get_customer_sqlite_client():
            return db
    
    db = await get_db_connection()
    
    assert db is not None
    assert isinstance(db, aiosqlite.Connection)
    assert db.row_factory == aiosqlite.Row
