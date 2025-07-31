import json
import os
from datetime import datetime

EVENTS_PATH = os.path.join(os.path.dirname(__file__), 'events', 'event_data.json')

def sort_events_json():
    with open(EVENTS_PATH, 'r', encoding='utf-8') as f:
        events = json.load(f)
    def event_date(e):
        try:
            return datetime.strptime(e.get('date', ''), '%d-%m-%Y')
        except:
            return datetime.max
    events_sorted = sorted(events, key=event_date)
    with open(EVENTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(events_sorted, f, indent=2, ensure_ascii=False)
    # print('event_data.json sorted by date.')

if __name__ == '__main__':
    sort_events_json()
