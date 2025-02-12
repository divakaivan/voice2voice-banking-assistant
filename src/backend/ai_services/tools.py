from typing import List, Dict

from datetime import datetime, timedelta
from loguru import logger
from pydantic_ai import RunContext

from backend.ai_services.agent import Dependencies
        
async def get_recent_transactions(ctx: RunContext[Dependencies], start_date: str = None, end_date: str = "2023-10-14", category: str = None, merchant: str = None, last_n: str = "5") -> List[Dict]:
    """
    Retrieve last n transactions based on optional filters for start date, end date, category, and merchant.

    Args:
        ctx: The context of the current run.
        start_date (str, optional): The start date (YYYY-MM-DD) for filtering transactions.
        end_date (str, optional): The end date (YYYY-MM-DD) for filtering transactions.
        category (str, optional): Filter by transaction category.
        merchant (str, optional): Filter by merchant name.
        last_n (str, optional): The number of transactions to return.

    Returns:
        list: A list of matching transactions.
    """
    query = """
        SELECT Transaction_Amount, Date, Merchant_Name, Category 
        FROM Ivanov_Transactions 
        WHERE 1=1
        """

    if start_date:
        query += f" AND strftime('%s', substr(Date, 7, 4) || '-' || substr(Date, 4, 2) || '-' || substr(Date, 1, 2)) >= strftime('%s', '{start_date}') "
    if end_date:
        query += f" AND strftime('%s', substr(Date, 7, 4) || '-' || substr(Date, 4, 2) || '-' || substr(Date, 1, 2)) <= strftime('%s', '{end_date}') "
    if category:
        query += f" AND Category = '{category}'"
    if merchant:
        query += f" AND Merchant_Name = '{merchant}'"
    if last_n:
        query += f" ORDER BY strftime('%s', substr(Date, 7, 4) || '-' || substr(Date, 4, 2) || '-' || substr(Date, 1, 2)) DESC LIMIT {last_n}"
    
    try:
        async for sqlite_db in ctx.deps.sqlite_db:
            logger.debug(f"Executing query: {query}")
            cursor = await sqlite_db.execute(query)
            rows = await cursor.fetchall()
            await cursor.close()
            results = [dict(row) for row in rows]

            return results
    except Exception as e:
        logger.error(f"Error executing query {query}. Error: {e}")
        return []
        
async def summarize_spending(
        ctx: RunContext[Dependencies], 
        time_period: str = "this week", 
        return_budget_status: bool = False,
        budget_limits: Dict[str, int] = {
            "Cosmetic": 20000,
            "Travel": 100000,
            "Clothing": 300000,
            "Electronics": 150000,
            "Restaurant": 200000,
            "Market": 100000
        }) -> Dict:
    """
    Summarize spending for a given time period by category.

    Args:
        ctx: The context of the current run.
        time_period (str): Time period to summarise(e.g., "last month", "this week").
        return_budget_status (bool): Whether to return budget status.
        budget_limits (dict): Budget limits per category.

    Returns:
        dict: A breakdown of spending by category.
    """

    if "last month" in time_period:
        start_date = "DATE('2023-10-14', '-1 month')"
    elif "this week" in time_period:
        start_date = "DATE('2023-10-14', '-7 days')"
    else:
        start_date = "DATE('2023-10-14', '-7 days')"

    query = f"""
        SELECT Category, SUM(Transaction_Amount) as total_spent 
        FROM Ivanov_Transactions 
        WHERE strftime('%s', substr(Date, 7, 4) || '-' || substr(Date, 4, 2) || '-' || substr(Date, 1, 2)) >= strftime('%s', {start_date})
        GROUP BY Category
        """
    try:
        logger.debug(f"Executing query: {query}")
        # async for sqlite_db in ctx.deps.sqlite_db:
        async for sqlite_db in ctx.deps.sqlite_db:
            cursor = await sqlite_db.execute(query)
            results = await cursor.fetchall()
            await cursor.close()
            results = {row[0]: row[1] for row in results}
            logger.debug(f"Results: {results}") 
            if return_budget_status:
                budget_results = {}
                for category, total_spent in results.items():
                    budget = budget_limits.get(category, float('inf'))
                    budget_results[category] = {
                        "spent": total_spent,
                        "budget": budget,
                        "status": "over budget" if total_spent > budget else "within budget"
                    }

                return budget_results
            else:
                return results

    except Exception as e:
        logger.error(f"Error executing query {query}. Error: {e}")
        return {}

async def detect_unusual_spending(ctx: RunContext[Dependencies], threshold: float = None, time_period: str = "last month", specific_month: str = None) -> list:
    """
    Identify transactions that deviate from past behavior.

    Args:
        ctx: The context of the current run.
        threshold (float, optional): Spending threshold multiplier (default is 1.5x avg spending).
        time_period (str, optional): The period to analyze (default is "last month", "this week", "January").
        specific_month (str, optional): A specific month to analyze (e.g., "2023-08").

    Returns:
        list: A list of flagged transactions.
    """
    if specific_month:
        month_date = datetime.strptime(specific_month, "%Y-%m")
        start_date = month_date.replace(day=1).strftime("%Y-%m-%d")
        end_date = (month_date.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1).strftime("%Y-%m-%d")
        date_filter = f" BETWEEN strftime('%s', '{start_date}') AND strftime('%s', '{end_date}')"
    elif "last month" in time_period:
        date_filter = ">= strftime('%s', DATE('2023-10-14', '-1 month'))"
    elif "this week" in time_period:
        date_filter = ">= strftime('%s', DATE('2023-10-14', '-7 days'))"
    else:
        date_filter = ">= strftime('%s', DATE('2023-10-14', '-1 month'))"

    avg_query = f"""
        SELECT AVG(Transaction_Amount) 
        FROM Ivanov_Transactions 
        WHERE strftime('%s', substr(Date, 7, 4) || '-' || substr(Date, 4, 2) || '-' || substr(Date, 1, 2)) {date_filter}
        """

    try:
        async for sqlite_db in ctx.deps.sqlite_db:
            logger.debug(f"Executing query: {avg_query}")
            avg_spending = await sqlite_db.execute(avg_query)
            avg_spending = await avg_spending.fetchone()
            avg_spending = avg_spending[0] if avg_spending else 0

            if avg_spending == 0:
                logger.debug("No transactions found for the specified time period.")
                return []

            threshold = threshold or avg_spending * 1.5

            query = f"""
                SELECT Transaction_Amount, Date, Merchant_Name, Category
                FROM Ivanov_Transactions 
                WHERE Transaction_Amount > {str(threshold)} AND strftime('%s', substr(Date, 7, 4) || '-' || substr(Date, 4, 2) || '-' || substr(Date, 1, 2)) >= strftime('%s', '{date_filter}')
                """
            logger.debug(f"Executing query: {query}")
            cursor = await sqlite_db.execute(query)
            rows = await cursor.fetchall()
            await cursor.close()
            results = [dict(row) for row in rows]

            return results
    except Exception as e:
        logger.error(f"Error executing query: {query}. Error: {e}")
        return []
