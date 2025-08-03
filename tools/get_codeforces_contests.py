import requests
from datetime import datetime, timedelta
from langchain.tools import tool

@tool
def get_codeforces_contests_on_date(date_str: str | None) -> dict:
    """
    Fetch Codeforces contests on a specific date (UTC), or all upcoming contests if no date is provided.
    Args:
        date_str: A string in format 'DD-MM-YYYY' (e.g., '05-08-2025'), or None/empty for all upcoming contests.
    Returns:
        A dictionary with a formatted list of contests or an error message.
    """
    url = "https://codeforces.com/api/contest.list"
    response = requests.get(url)
    if response.status_code != 200:
        return {"status": "error", "message": f"Failed to fetch data: {response.status_code}"}

    data = response.json()
    if data.get("status") != "OK":
        return {"status": "error", "message": "API returned an error"}

    contests = data["result"]
    upcoming = [c for c in contests if c.get("phase") == "BEFORE"]

    matched = []
    # helper to convert UTC timestamp to IST
    def to_ist(ts: int) -> datetime:
        utc_dt = datetime.utcfromtimestamp(ts)
        return utc_dt + timedelta(hours=5, minutes=30)

    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%d-%m-%Y").date()
        except ValueError:
            return {"status": "error", "message": "Invalid date format. Use DD-MM-YYYY."}

        for contest in upcoming:
            ist_start = to_ist(contest["startTimeSeconds"])
            if ist_start.date() == target_date:
                date_fmt = ist_start.strftime("%d-%m-%Y")
                time_fmt = ist_start.strftime("%I:%M %p IST")
                matched.append(f"{contest['name']}, {date_fmt}, {time_fmt}")
        return {"status": "ok", "date": date_str, "contests": matched}

    # no date filter: return all upcoming
    for contest in upcoming:
        ist_start = to_ist(contest["startTimeSeconds"])
        date_fmt = ist_start.strftime("%d-%m-%Y")
        time_fmt = ist_start.strftime("%I:%M %p IST")
        matched.append(f"{contest['name']}, {date_fmt}, {time_fmt}")

    return {"status": "ok", "contests": matched}
