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
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").strftime("%d-%m-%Y")
    except ValueError:
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
def find_event(event_name: str, date: str | None) -> str:
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
    event_name = event_name.strip().lower()
    date = normalize_date(date) if date else None
    if not os.path.exists(EVENTS_FILE):
        return "❌ Event file not found."

    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except json.JSONDecodeError:
        return "❌ Failed to load events. The file may be corrupted."

    # Filter by date if provided
    filtered_events = [e for e in events if (not date or e.get("date") == date)]
    event_names = [e.get("event_name", "").strip().lower() for e in filtered_events]

    if not event_names:
        return None

    # Find most similar event name
    best_name, score = get_most_similar_event(event_name, event_names)
    if score < 0.5:  # You can adjust this threshold
        return None

    for e in filtered_events:
        if e.get("event_name", "").strip().lower() == best_name:
            # Add similarity score to the event dict
            event_json = dict(e)
            event_json["similarity"] = round(float(score), 2)
            return json.dumps(event_json, ensure_ascii=False, indent=2)
    # If no event found, return a JSON error message
    return json.dumps({"error": "No matching event found."}, ensure_ascii=False, indent=2)