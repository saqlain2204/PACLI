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
def find_and_edit_event(event_name: str, field_to_edit: str, new_value: str, date: str | None) -> str:
    """
    Find an event by name and automatically edit a specified field in it.
    
    Args:
        event_name: Name of the event to find and edit.
        field_to_edit: The field to edit (e.g., time, date).
        new_value: The new value for the field.
        
    Returns:
        Result of the edit operation.
    """
    # First find the event
    date_arg = normalize_date(date) if date else None
    found_json = find_event.invoke({"event_name": event_name, "date": date_arg})
    if "error" in found_json:
        return "❌ Event not found. Please check the event name or date."
    found_data = json.loads(found_json)

    if not found_data or (date and found_data.get("date") != date):
        return "Event not found or invalid response from find_event."

    if not date:
        date = found_data["date"]
    
    print(f"Found event: {found_data}")
    event_name = found_data["event_name"]
    
    if field_to_edit.lower() == "date":
        new_value = normalize_date(new_value)
        if not new_value:
            return "Invalid date format. Please use DD-MM-YYYY."

    # Call edit_event with extracted info
    result = edit_event.invoke({
        "event_name": event_name,
        "date": date,
        "field_to_edit": field_to_edit,
        "new_value": new_value
    })
    return result
