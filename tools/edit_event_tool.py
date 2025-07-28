from langchain.tools import tool
import json
import os

EVENTS_FILE = "events/event_data.json"

@tool
def edit_event(event_name: str, date: str, field_to_edit: str, new_value: str = "") -> str:
    """
    Edit or delete an existing event in the event_data.json file based on event name and date.

    Args:
        event_name: Name of the event to match.
        date: Date of the event to match (format: DD-MM-YYYY).
        field_to_edit: The field to update (e.g., 'time', 'extra_info').
                       To delete the event, pass 'delete'.
        new_value: The new value to assign to the specified field (ignored for delete).

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
        if event.get("event_name") == event_name and event.get("date") == date:
            if field_to_edit.lower() == "delete":
                updated = True  # Don't append this event to the new list
                continue
            elif field_to_edit in event:
                event[field_to_edit] = new_value
                updated = True
        new_events.append(event)

    if not updated:
        return f"❌ No event found with name '{event_name}' on '{date}', or field '{field_to_edit}' not valid."

    try:
        with open(EVENTS_FILE, "w") as f:
            json.dump(new_events, f, indent=4)

        if field_to_edit.lower() == "delete":
            return f"🗑️ Successfully deleted event '{event_name}' on {date}."
        else:
            return f"✅ Updated '{field_to_edit}' of event '{event_name}' on {date} to '{new_value}'."

    except Exception as e:
        return f"❌ Failed to save updated events: {e}"
