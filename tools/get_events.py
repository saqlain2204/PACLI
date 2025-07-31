from langchain.tools import tool
from datetime import datetime
import json
import os

EVENTS_FILE = "events/event_data.json"

@tool
def get_event_schedule(start_date_str: str, end_date_str: str) -> dict:
    """
    Retrieve events scheduled within a date range from the local JSON file.
    Args:
        start_date_str: Start date string in DD-MM-YYYY format.
        end_date_str: End date string in DD-MM-YYYY format.
    Returns:
        A structured JSON dictionary with matching events or error message.
    """
    try:
        start_date = datetime.strptime(start_date_str, "%d-%m-%Y").date()
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y").date()
    except Exception:
        return {
            "status": "error",
            "message": "Invalid date format. Please use DD-MM-YYYY."
        }

    if not os.path.exists(EVENTS_FILE):
        return {
            "status": "error",
            "message": "No events have been scheduled yet."
        }

    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except json.JSONDecodeError:
        return {
            "status": "error",
            "message": "Event file is corrupted or empty."
        }

    matched_events = []
    for event in events:
        try:
            event_date = datetime.strptime(event["date"], "%d-%m-%Y").date()
            if start_date <= event_date <= end_date:
                matched_events.append({
                    "event_name": event.get("event_name", ""),
                    "date": event.get("date", ""),
                    "day": event.get("day", ""),
                    "month": event.get("month", ""),
                    "year": event.get("year", ""),
                    "time": event.get("time", ""),
                    "extra_info": event.get("extra_info", ""),
                    "public": event.get("public", False)
                })
        except Exception:
            continue

    if not matched_events:
        return {
            "status": "error",
            "message": f"No events scheduled from {start_date.strftime('%A, %B %d')} to {end_date.strftime('%A, %B %d')}."
        }

    return {
        "status": "ok",
        "start_date": start_date_str,
        "end_date": end_date_str,
        "events": matched_events
    }
