# tools/event_scheduler.py

import json
import os
from datetime import datetime
from langchain.tools import tool

# Path to events/event_data.json
EVENTS_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'events', 'event_data.json')

@tool
def schedule_event(date: str, time: str | None, event_name: str, extra_info: str = "", public: bool = None) -> str:
    """
    Schedule an event and store it in a JSON file.

    Parameters:
    - date: Date in format YYYY-MM-DD
    - time: Time (e.g., "10:00 AM")
    - event_name: Description or title of the event
    - extra_info: Any additional info to store
    """

    # Convert date into components
    try:
        date_obj = datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        return "❌ Invalid date format. Use DD-MM-YYYY."

    if not time:
        time = ""
    formatted_event = {
        "event_name": event_name,
        "date": date_obj.strftime("%d-%m-%Y"),
        "day": date_obj.strftime("%A"),
        "month": date_obj.strftime("%B"),
        "year": date_obj.year,
        "time": time,
        "extra_info": extra_info or "None",
        "public": public if public is not None else True  # Default to public if not specified
    }

    # Load existing events
    if os.path.exists(EVENTS_FILE_PATH):
        with open(EVENTS_FILE_PATH, 'r') as f:
            try:
                events = json.load(f)
            except json.JSONDecodeError:
                events = []
    else:
        events = []

    # Append and save
    events.append(formatted_event)
    with open(EVENTS_FILE_PATH, 'w') as f:
        json.dump(events, f, indent=2)

    return f"✅ Event scheduled: {event_name} on {formatted_event['date']} at {time}"
