import os.path
import aiosqlite

async def get_customer_sqlite_client():
    """
    Return a database connection for use as a dependency.
    This connection has the Row row factory automatically attached.
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "transactions.db")
    db = await aiosqlite.connect(db_path)
    db.row_factory = aiosqlite.Row

    yield db
    # try:
    #     yield db
    # finally:
    #     await db.close()
