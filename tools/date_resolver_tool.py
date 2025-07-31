from langchain.tools import tool
from datetime import datetime
import dateparser

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
    return {"day": dt.strftime("%A")}

@tool
def resolve_date_from_phrase(phrase: str) -> str:
    """
    Convert a natural language date phrase (e.g., 'next Sunday', 'this Friday') to a date string (DD-MM-YYYY).
    Args:
        phrase (str): Natural language date phrase.
    Returns:
        str: Date string in DD-MM-YYYY format, or error message.
    """
    dt = dateparser.parse(phrase)
    if not dt:
        return "Could not parse the date phrase. Please try a different format."
    return {"date": dt.strftime("%d-%m-%Y")}
