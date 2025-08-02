from langchain.tools import tool
from tools.find_event_tool import find_event
from tools.edit_event_tool import edit_event
import json
from datetime import datetime

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

@tool
def find_and_edit_event(event_name: str, field_to_edit: str, new_value: str | bool, date: str = "", time: str | None = "") -> str:
    """
    Find an event by name and automatically edit a specified field in it.
    
    Args:
        event_name: Name of the event to find and edit.
        field_to_edit: The field to edit (e.g., time, date).
        new_value: The new value for the field.
        date: (Optional) Date of the event in 'DD-MM-YYYY' format. If not provided, it will search for the event without date filtering.
        time: (Optional) Time of the event to filter by. If provided, it will only edit events that match this time.
        
    Returns:
        Result of the edit operation.
    """
    # Always pass a string for date (empty string if not provided)
    date_arg = normalize_date(date) if date else ""
    # Ensure date is always a string, never None
    date_arg_str = date_arg if date_arg is not None else ""
    time_arg = time if time is not None else ""
    found_json = find_event.invoke({"event_name": event_name, "date": date_arg_str, "time": time_arg})
    if "error" in found_json:
        return "❌ Event not found. Please check the event name or date."
    found_data = json.loads(found_json)

    if not found_data or (isinstance(found_data, list) and len(found_data) == 0):
        return "Event not found or invalid response from find_event."

    if isinstance(found_data, list):
        events_to_edit = found_data
    else:
        events_to_edit = [found_data]

    results = []
    for event in events_to_edit:
        edit_date = event.get("date")
        edit_name = event.get("event_name")
        edit_time = event.get("time")
        if not edit_name:
            continue
        if not edit_date or not edit_name:
            continue
        if field_to_edit.lower() == "date":
            new_value_norm = normalize_date(new_value)
            if not new_value_norm:
                results.append("Invalid date format. Please use DD-MM-YYYY.")
                continue
            new_value_to_use = new_value_norm
        else:
            new_value_to_use = new_value
        result = edit_event.invoke({
            "event_name": edit_name,
            "time": edit_time,
            "date": edit_date,
            "field_to_edit": field_to_edit,
            "new_value": new_value_to_use
        })
        if result is not None:
            results.append(str(result))
    if not results:
        return "No matching events found to edit."
    return "\n".join(results)
