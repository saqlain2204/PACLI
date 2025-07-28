from langchain.tools import tool
from datetime import datetime, timedelta
import json
import os
import re

EVENTS_FILE = "events/event_data.json"

def parse_time_range(time_range: str):
    """
    Parse time_range like 'next 2 weeks', 'next 5 days', 'next week', etc.
    Returns (start_date, end_date) as date objects.
    """
    today = datetime.today().date()
    match = re.match(r"next (\d+) (week|weeks|day|days)", time_range.lower())
    if match:
        num = int(match.group(1))
        unit = match.group(2)
        if "week" in unit:
            start = today + timedelta(days=(7 - today.weekday()))  # Next Monday
            end = start + timedelta(days=7 * num - 1)
        else:
            start = today + timedelta(days=1)
            end = start + timedelta(days=num - 1)
        return start, end
    elif time_range.lower() == "next week":
        start = today + timedelta(days=(7 - today.weekday()))
        end = start + timedelta(days=6)
        return start, end
    elif time_range.lower() == "this week":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start, end
    else:
        return None, None

@tool
def get_event_schedule(time_range: str = "next_week") -> str:
    """
    Retrieve events within a flexible time range from the local JSON file.

    Args:
        time_range: e.g. 'next week', 'next 2 weeks', 'next 5 days', 'this week', etc.

    Returns:
        A human-readable string of scheduled events in that time range.
    """
    start_date, end_date = parse_time_range(time_range)
    if not start_date or not end_date:
        return None

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
            if start_date <= event_date <= end_date:
                matched_events.append(
                    f"📌 {event['event_name']} — {event['day']}, {event['date']} at {event['time']}"
                )
        except Exception:
            continue

    if not matched_events:
        return f"📅 No events scheduled from {start_date.strftime('%A, %B %d')} to {end_date.strftime('%A, %B %d')}."

    return f"📅 Events from {start_date.strftime('%A, %B %d')} to {end_date.strftime('%A, %B %d')}:\n" + "\n".join(matched_events)