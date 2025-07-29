
from langchain.tools import tool
from datetime import datetime
import json
import os

EVENTS_FILE = "events/event_data.json"

@tool
def get_event_schedule(date_str: str) -> str:
    """
    Retrieve events scheduled on a specific date from the local JSON file.

    Args:
        date_str: Date string in DD-MM-YYYY format (resolved from natural language).

    Returns:
        A human-readable string of scheduled events on that date.
    """
    try:
        search_date = datetime.strptime(date_str, "%d-%m-%Y").date()
    except Exception:
        return "Invalid date format. Please use DD-MM-YYYY."

    if not os.path.exists(EVENTS_FILE):
        return "📭 No events have been scheduled yet."

    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except json.JSONDecodeError:
        return "⚠️ Event file is corrupted or empty."

    matched_events = []
    for event in events:
        try:
            event_date = datetime.strptime(event["date"], "%d-%m-%Y").date()
            if event_date == search_date:
                matched_events.append(
                    f"📌 {event['event_name']} — {event['day']}, {event['date']} at {event['time']}"
                )
        except Exception:
            continue

    if not matched_events:
        return f"📅 No events scheduled for {search_date.strftime('%A, %B %d')}."

    return f"📅 Events for {search_date.strftime('%A, %B %d')}:\n" + "\n".join(matched_events)