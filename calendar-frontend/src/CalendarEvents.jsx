import React, { useState, useEffect } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";
import './calendar-custom.css';

function formatDate(date) {
  // Format date as DD-MM-YYYY
  const d = date.getDate().toString().padStart(2, "0");
  const m = (date.getMonth() + 1).toString().padStart(2, "0");
  const y = date.getFullYear();
  return `${d}-${m}-${y}`;
}

function CalendarEvents() {
  const [selectedDate, setSelectedDate] = useState(null);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState("");

  // Use local network IP for event data fetch
  const EVENTS_API_URL = window.location.hostname === "localhost"
    ? "http://localhost:8000/events/event_data.json"
    : `http://${window.location.hostname}:8000/events/event_data.json`;

  // Fetch events from backend
  const fetchEvents = () => {
    setLoading(true);
    setError(null);
    fetch(EVENTS_API_URL)
      .then(res => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
      })
      .then(data => {
        setEvents(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(err => {
        setError("Failed to fetch events. Check server and CORS.");
        setEvents([]);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchEvents();
  }, []);

  // Listen for SSE updates and show persistent toast, refetch events on update
  useEffect(() => {
    const streamUrl = window.location.hostname === "localhost"
      ? "http://localhost:8000/events/stream"
      : `http://${window.location.hostname}:8000/events/stream`;
    const eventSource = new window.EventSource(streamUrl);
    eventSource.onmessage = (e) => {
      if (e.data === 'updated') {
        setToastMessage('Event data updated!');
        setShowToast(true);
        fetchEvents(); // Refetch events when backend notifies update
      }
    };
    return () => eventSource.close();
  }, []);

  // Get all events for the selected month, sorted by date
  const eventsForMonth = selectedDate
    ? events
        .filter(e => {
          const [d, m, y] = e.date.split("-");
          return (
            parseInt(m, 10) === selectedDate.getMonth() + 1 &&
            parseInt(y, 10) === selectedDate.getFullYear()
          );
        })
        .sort((a, b) => {
          // Sort by date (DD-MM-YYYY)
          const [ad, am, ay] = a.date.split("-").map(Number);
          const [bd, bm, by] = b.date.split("-").map(Number);
          const aDate = new Date(ay, am - 1, ad);
          const bDate = new Date(by, bm - 1, bd);
          return aDate - bDate;
        })
    : [];

  // Get events for the selected date
  const eventsForDate = selectedDate
    ? events.filter(e => e.date === formatDate(selectedDate))
    : [];

  // Mark dates with events
  const eventDatesSet = new Set(events.map(e => e.date));

  // Custom tile content for calendar (green dot for event days)
  function tileContent({ date, view }) {
    if (view === 'month') {
      const d = formatDate(date);
      if (eventDatesSet.has(d)) {
        return <span className="event-dot" title="Event" />;
      }
    }
    return null;
  }

  // Custom tile class for event highlight and weekends
  function tileClassName({ date, view }) {
    if (view === 'month') {
      const d = formatDate(date);
      const day = date.getDay(); // 0 = Sunday, 6 = Saturday
      if (day === 0 || day === 6) {
        return 'weekend-day';
      }
      if (eventDatesSet.has(d)) {
        return 'event-day';
      }
    }
    return null;
  }

  return (
    <div className="calendar-container">
      {showToast && (
        <div className="toast">
          {toastMessage} <button onClick={() => setShowToast(false)}>Dismiss</button>
        </div>
      )}
      <h2 className="calendar-title">Event Calendar</h2>
      <Calendar
        onClickDay={setSelectedDate}
        tileContent={tileContent}
        tileClassName={tileClassName}
        className="custom-calendar"
      />
      <div className="calendar-events-section">
        <h3>Events for {selectedDate ? formatDate(selectedDate) : "..."}:</h3>
        {loading && <div>Loading events...</div>}
        {error && <div style={{ color: "red" }}>{error}</div>}
        {!loading && !error && selectedDate && eventsForDate.length === 0 && (
          <div className="no-events">No events for this day.</div>
        )}
        <ul className="event-list">
          {eventsForDate.map(e => (
            <li key={e.event_name + e.date} className="event-item">
              <strong>{e.event_name}</strong>
              {e.time && e.time !== 'None' && <span className="event-time">({e.time})</span>}<br />
              {e.extra_info && e.extra_info !== 'None' && <span className="event-extra">{e.extra_info}</span>}
            </li>
          ))}
        </ul>
      </div>
      <div className="calendar-month-summary">
        <h4>Events this month: {eventsForMonth.length}</h4>
        <ul className="event-list">
          {eventsForMonth.map(e => (
            <li key={e.event_name + e.date} className="event-item">
              <div style={{display: 'flex', alignItems: 'center', width: '100%'}}>
                <strong style={{flex: 1}}>{e.event_name}</strong>
                <span className="event-date">{e.date}</span>
              </div>
              {e.time && e.time !== 'None' && (
                <div className="event-time-section">
                  <span className="event-time-label">Time:</span>
                  <span className="event-time">{e.time}</span>
                </div>
              )}
              {e.extra_info && e.extra_info !== 'None' && <span className="event-extra">{e.extra_info}</span>}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default CalendarEvents;
