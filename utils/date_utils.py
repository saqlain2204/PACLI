from datetime import datetime, timedelta

from datetime import datetime, timedelta

def get_next_weekday(target_weekday: int, from_date: datetime = None) -> datetime:
    """
    Get the date of the next target_weekday from from_date (default: today).
    target_weekday: 0 = Monday, ..., 6 = Sunday
    """
    if from_date is None:
        from_date = datetime.today()

    days_ahead = (target_weekday - from_date.weekday() + 7) % 7
    days_ahead = 7 if days_ahead == 0 else days_ahead
    return from_date + timedelta(days=days_ahead)




def get_next_week_range() -> tuple:
    """
    Get the start (next Monday) and end (next Sunday) dates of the upcoming week.

    Returns:
        A tuple of (start_date, end_date) as date objects.
    """
    today = datetime.now()
    days_ahead = (7 - today.weekday()) % 7
    days_ahead = days_ahead if days_ahead != 0 else 7  # ensure it's always future

    next_monday = today + timedelta(days=days_ahead)
    next_sunday = next_monday + timedelta(days=6)

    return next_monday.date(), next_sunday.date()
