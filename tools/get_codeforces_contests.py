import requests
from datetime import datetime
from langchain.tools import tool

@tool
def get_codeforces_contests_on_date(date_str: str | None) -> dict:
    """
    Fetch Codeforces contests on a specific date (UTC), or all upcoming contests if no date is provided.
    Args:
        date_str: A string in format 'DD-MM-YYYY' (e.g., '05-08-2025'), or None/empty for all upcoming contests.
    Returns:
        A dictionary with a list of contests or error message.
    """
    url = "https://codeforces.com/api/contest.list"
    response = requests.get(url)
    if response.status_code != 200:
        return {"status": "error", "message": f"Failed to fetch data: {response.status_code}"}
    
    data = response.json()
    if data["status"] != "OK":
        return {"status": "error", "message": "API returned an error"}

    contests = data["result"]
    upcoming = [c for c in contests if c["phase"] == "BEFORE"]

    matched = []
    if date_str:
        try:
            target_date = datetime.strptime(date_str, "%d-%m-%Y").date()
        except ValueError:
            return {"status": "error", "message": "Invalid date format. Use DD-MM-YYYY."}
        
        for contest in upcoming:
            start_time = datetime.utcfromtimestamp(contest["startTimeSeconds"])
            if start_time.date() == target_date:
                matched.append({
                    "name": contest["name"],
                    "start_time": start_time.strftime("%d-%m-%Y %I:%M %p UTC"),
                    "duration_hours": contest["durationSeconds"] // 3600
                })
        return {
            "status": "ok",
            "date": date_str,
            "contests": matched
        }
    else:
        for contest in upcoming:
            start_time = datetime.utcfromtimestamp(contest["startTimeSeconds"])
            matched.append({
                "name": contest["name"],
                "start_time": start_time.strftime("%d-%m-%Y %I:%M %p UTC"),
                "duration_hours": contest["durationSeconds"] // 3600
            })
        return {
            "status": "ok",
            "contests": matched
        }
