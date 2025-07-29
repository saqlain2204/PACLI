
from langchain.tools import tool
from datetime import datetime
import json
import os

EVENTS_FILE = "events/event_data.json"

@tool
def get_event_schedule(start_date_str: str, end_date_str: str) -> str:
    """
    Retrieve events scheduled within a date range from the local JSON file.

    Args:
        start_date_str: Start date string in DD-MM-YYYY format.
        end_date_str: End date string in DD-MM-YYYY format.

    Returns:
        A human-readable string of scheduled events in that range.
    """
    try:
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y").date()
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y").date()
    except Exception:
        return "Error: Invalid date format. Please use DD-MM-YYYY."

    if not os.path.exists(EVENTS_FILE):
        return "Error: No events have been scheduled yet."

    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except json.JSONDecodeError:
        return "Error: Event file is corrupted or empty."

    matched_events = []
    for event in events:
        try:
            event_date = datetime.strptime(event["date"], "%d-%m-%Y").date()
            if start_date <= event_date <= end_date:
                matched_events.append(
                    f"📌 {event['event_name']} — {event['day']}, {event['date']} at {event['time']}"
                )
        except Exception:
            continue

    if not matched_events:
        return f"Error: No events scheduled from {start_date.strftime('%A, %B %d')} to {end_date.strftime('%A, %B %d')}."

    return f"📅 Events from {start_date.strftime('%A, %B %d')} to {end_date.strftime('%A, %B %d')}:\n" + "\n".join(matched_events)