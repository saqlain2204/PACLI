from langchain.tools import tool
from datetime import datetime

@tool
def resolve_day_from_date(date_str: str) -> str:
    """
    Convert a date string (DD-MM-YYYY or YYYY-MM-DD) to the corresponding day of the week.
    Args:
        date_str (str): Date string in DD-MM-YYYY or YYYY-MM-DD format.
    Returns:
        str: Day of the week (e.g., Monday, Tuesday).
    """
    # Try DD-MM-YYYY first
    try:
        dt = datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return "Invalid date format. Please use DD-MM-YYYY or YYYY-MM-DD."
    return dt.strftime("%A")
