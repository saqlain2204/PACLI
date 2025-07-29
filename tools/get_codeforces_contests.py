import requests
from datetime import datetime
from langchain.tools import tool

@tool
def get_codeforces_contests_on_date(date_str: str | None) -> str:
    """
    Fetch Codeforces contests on a specific date (UTC), or all upcoming contests if no date is provided.
    Args:
        date_str: A string in format 'YYYY-MM-DD' (e.g., '2025-08-05'), or None/empty for all upcoming contests.
    Returns:
        List of contests on that date, or all upcoming contests.
    """
    url = "https://codeforces.com/api/contest.list"
    response = requests.get(url)
    if response.status_code != 200:
        return f"❌ Failed to fetch data: {response.status_code}"
    data = response.json()
    if data["status"] != "OK":
        return "❌ API returned an error"

    contests = data["result"]
    upcoming = [c for c in contests if c["phase"] == "BEFORE"]

    matched = []
    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return "❌ Invalid date format. Use YYYY-MM-DD."
        for contest in upcoming:
            start_time = datetime.utcfromtimestamp(contest["startTimeSeconds"])
            if start_time.date() == target_date:
                name = contest["name"]
                start_str = start_time.strftime("%Y-%m-%d %H:%M UTC")
                duration = contest["durationSeconds"] // 3600
                matched.append(f"{name} | Starts: {start_str} | Duration: {duration} hrs")
        return "\n".join(matched) if matched else f"No contests on {date_str}."
    else:
        for contest in upcoming:
            start_time = datetime.utcfromtimestamp(contest["startTimeSeconds"])
            name = contest["name"]
            start_str = start_time.strftime("%Y-%m-%d %H:%M UTC")
            duration = contest["durationSeconds"] // 3600
            matched.append(f"{name} | Starts: {start_str} | Duration: {duration} hrs")
        return "\n".join(matched) if matched else "No upcoming contests found."

