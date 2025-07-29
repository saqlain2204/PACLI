# Calendar Frontend

A minimal React calendar UI that displays events from your event_data.json file.

## How to use

1. Make sure you have Node.js and npm installed.

2. In your backend folder (where `events/event_data.json` is), run:

```sh
python -m http.server 8000
```

This will serve your event data at `http://localhost:8000/events/event_data.json`.

3. In the `calendar-frontend` directory, run:

```sh
npm install
npm start
```

4. The app will open in your browser. Click any date to see events for that day. The calendar will always show the latest events from your backend file.

## Tech stack
- React
- react-calendar

## Customization
- Edit `event_data.json` to add or change events.
- UI is in `src/CalendarEvents.jsx`.

---
Enjoy your calendar!
