from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_core.tools import tool
import json
import os
from datetime import datetime

EVENTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'events', 'event_data.json')

def normalize_date(date_str):
    """
    Normalize a date string to 'DD-MM-YYYY' format.
    If the date is already in this format, it returns as is.
    Args:
        date_str (str): Input date string in any common format.
    Returns:
        str or None: Normalized date string in 'DD-MM-YYYY' format, or None if parsing fails.
    """
    if not date_str:
        return None
    # If it's a datetime object, convert to string
    if isinstance(date_str, datetime):
        return date_str.strftime("%d-%m-%Y")
    # If it's not a string, try to convert
    if not isinstance(date_str, str):
        try:
            date_str = str(date_str)
        except Exception:
            return None
    # Try common formats
    for fmt in ["%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]:
        try:
            return datetime.strptime(date_str, fmt).strftime("%d-%m-%Y")
        except ValueError:
            continue
    return None

def get_most_similar_event(query, event_names):
    """
    Find the most similar event name to the query using cosine similarity.
    Args:
        query (str): The event name to search for.
        event_names (list of str): List of event names from the database.
    Returns:
        tuple: (best matching event name, similarity score)
    """
    vectorizer = TfidfVectorizer().fit(event_names + [query])
    vectors = vectorizer.transform(event_names + [query])
    similarities = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
    best_idx = similarities.argmax()
    return event_names[best_idx], similarities[best_idx]

@tool
def find_event(event_name: str, date) -> str:
    """
    Find a scheduled event by name and optionally by date, using string similarity if needed.
    If date is provided, only events on that date are considered. If not, all events are considered.
    Uses cosine similarity to find the closest event name match.
    Args:
        event_name (str): Name of the event to search for.
        date (str or None): Date of the event (format: DD-MM-YYYY) or None.
    Returns:
        str or None: Formatted string with event details if found, otherwise None.
    """
    event_name = event_name.strip().lower() if event_name else None
    # Ensure date is a string before normalization
    if date is not None and not isinstance(date, str):
        try:
            date = str(date)
        except Exception:
            date = None
    date = normalize_date(date) if date else None
    if not os.path.exists(EVENTS_FILE):
        return "❌ Event file not found."

    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except json.JSONDecodeError:
        return "❌ Failed to load events. The file may be corrupted."

    # Match events using all provided fields
    def matches(event, name, date, time=None, extra_info=None):
        if name and event.get("event_name", "").strip().lower() != name:
            return False
        if date and event.get("date") != date:
            return False
        if time and event.get("time", "") != time:
            return False
        if extra_info and event.get("extra_info", "") != extra_info:
            return False
        return True

    # Try to match with all fields if provided
    matched_events = []
    for e in events:
        if matches(e, event_name, date, e.get("time", None), e.get("extra_info", None)):
            matched_events.append(e)

    # If no exact match, fallback to fuzzy name/date match
    if not matched_events:
        filtered_events = [e for e in events if (not date or e.get("date") == date)]
        event_names = [e.get("event_name", "").strip().lower() for e in filtered_events]
        if not event_names:
            return json.dumps({"error": "No events found for the specified date." if date else "No events found."}, ensure_ascii=False, indent=2)
        best_name, score = get_most_similar_event(event_name, event_names)
        if score < 0.5:
            return json.dumps({"error": "No matching event found."}, ensure_ascii=False, indent=2)
        for e in filtered_events:
            if e.get("event_name", "").strip().lower() == best_name:
                event_json = dict(e)
                event_json["similarity"] = round(float(score), 2)
                return json.dumps(event_json, ensure_ascii=False, indent=2)
        return json.dumps({"error": "No matching event found."}, ensure_ascii=False, indent=2)

    # Return all matched events
    return json.dumps(matched_events, ensure_ascii=False, indent=2)