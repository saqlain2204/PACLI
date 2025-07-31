from langchain_core.tools import tool
from datetime import datetime
from rapidfuzz import process, fuzz
import json
import os

EVENTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'events', 'event_data.json')

def normalize_date(date_str):
    if not date_str:
        return None
    if isinstance(date_str, datetime):
        return date_str.strftime("%d-%m-%Y")
    if not isinstance(date_str, str):
        date_str = str(date_str)
    for fmt in ["%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]:
        try:
            return datetime.strptime(date_str, fmt).strftime("%d-%m-%Y")
        except ValueError:
            continue
    return None

@tool
def find_event(event_name: str = "", date: str = "") -> str:
    """
    Find a scheduled event using fuzzy matching by name, optionally filtered by date.
    Args:
        event_name (str): Partial or full event name (case insensitive).
        date (str): Optional date in DD-MM-YYYY format.
    Returns:
        str: JSON string of the best matching event or list of matches.
    """
    if not os.path.exists(EVENTS_FILE):
        return "❌ Event file not found."

    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except json.JSONDecodeError:
        return "❌ Failed to load events. File might be corrupted."

    normalized_date = normalize_date(date) if date else None
    query_name = event_name.strip().lower() if event_name and event_name.strip() else None

    filtered = events
    if normalized_date:
        filtered = [e for e in filtered if e.get("date") == normalized_date]
        if not filtered:
            return json.dumps({"error": f"No events found on {normalized_date}."}, indent=2)

    if query_name:
        name_map = {e["event_name"]: e for e in filtered if "event_name" in e}
        matches = process.extract(
            query_name,
            name_map.keys(),
            scorer=fuzz.WRatio,
            limit=3
        )
        if not matches or matches[0][1] < 60:
            return json.dumps({"error": "No matching event found."}, indent=2)

        best_match_name, score, _ = matches[0]
        best_event = name_map[best_match_name]
        best_event["match_score"] = score
        return json.dumps(best_event, indent=2, ensure_ascii=False)

    # If only date was given (no event name), return all events that day
    if normalized_date:
        return json.dumps(filtered, indent=2, ensure_ascii=False)

    return json.dumps({"error": "Please provide an event name or date."}, indent=2)
