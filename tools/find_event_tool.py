from datetime import date, datetime
from langchain.tools import tool
import json
import os

EVENTS_FILE = "events/event_data.json"

def normalize_date(date_str):
    """
    Normalize a date string to DD-MM-YYYY format.
    Accepts common formats like YYYY-MM-DD, DD/MM/YYYY, etc.
    Returns normalized string or original if parsing fails.
    """
    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%d-%m-%Y")
        except ValueError:
            continue
    return date_str.strip()

@tool
def find_event(event_name: str, date: str) -> str:
    """
    Find a scheduled event by name and date.

    Args:
        event_name: Name of the event to search for.
        date: Date of the event (format: DD-MM-YYYY).

    Returns:
        A formatted string with the event details if found, otherwise an error message.
    """
    event_name = event_name.strip().lower()
    date = normalize_date(date)
    if not os.path.exists(EVENTS_FILE):
        return "❌ Event file not found."

    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except json.JSONDecodeError:
        return "❌ Failed to load events. The file may be corrupted."

    for event in events:
        if event.get("event_name").strip().lower() == event_name and event.get("date") == date:
            details = "\n".join([f"{key.capitalize().replace('_', ' ')}: {value}" for key, value in event.items()])
            return f"✅ Found event:\n\n{details}"

    return None
