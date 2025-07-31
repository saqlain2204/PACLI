from langchain.tools import tool
import json
import os
from tools.date_resolver_tool import resolve_day_from_date

EVENTS_FILE = "events/event_data.json"

@tool
def edit_event(event_name: str, date: str | None, field_to_edit: str, time: str | None, new_value: str | bool = "") -> str:
    """
    Edit or delete an existing event in the event_data.json file based on event name and date.

    Args:
        event_name: Name of the event to match. pass it from the `find_event` tool. 
        date: Date of the event to match (format: DD-MM-YYYY).
        field_to_edit: The field to update (e.g., 'time', 'extra_info'). To delete the event, pass 'delete'.
        new_value: The new value to assign to the specified field (ignored for delete) if it is date, it should be in 'DD-MM-YYYY' format.
        time: Time of the event to match (optional, if not provided, it will match any time).

    Returns:
        A confirmation message about the edit or deletion.
    """
    if not os.path.exists(EVENTS_FILE):
        return "❌ Event file not found."

    try:
        with open(EVENTS_FILE, "r") as f:
            events = json.load(f)
    except json.JSONDecodeError:
        return "❌ Failed to load events. The file may be corrupted."

    updated = False
    new_events = []
    for event in events:
        match = (
            event.get("event_name") == event_name and
            event.get("date") == date and
            (time is None or time == "" or event.get("time") == time)
        )
        if match:
            if field_to_edit.lower() == "delete":
                updated = True  # Don't append this event to the new list
                continue
            elif field_to_edit.lower() == "date":
                if not new_value:
                    return "Invalid date format. Please use DD-MM-YYYY."
                event["date"] = new_value
                event["day"] = resolve_day_from_date(new_value)
                updated = True
            elif field_to_edit in event:
                event[field_to_edit] = new_value
                updated = True
        new_events.append(event)

    if not updated:
        return None

    try:
        with open(EVENTS_FILE, "w") as f:
            json.dump(new_events, f, indent=4)
            
        if field_to_edit.lower() == "delete":
            return f"🗑️ Successfully deleted event '{event_name}' on {date}."
        else:
            return f"✅ Updated '{field_to_edit}' of event '{event_name}' on {date} to '{new_value}'."

    except Exception as e:
        return f"❌ Failed to save updated events: {e}"
