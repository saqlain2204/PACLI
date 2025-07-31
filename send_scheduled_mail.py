import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import json

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
MY_EMAIL = os.getenv('MY_EMAIL')
# RECIPIENT_EMAIL can be a comma-separated string
RECIPIENT_EMAILS = os.getenv('RECIPIENT_EMAIL', '').split(',')
RECIPIENT_EMAILS = [email.strip() for email in RECIPIENT_EMAILS if email.strip()]

EVENTS_PATH = os.path.join(os.path.dirname(__file__), 'events/event_data.json')

def format_html_email(events, date):
    if not events:
        return f"""
        <div style='font-family:Segoe UI,Roboto,Arial,sans-serif;padding:24px;'>
            <h2 style='color:#222;'>No events scheduled for <span style='color:#3182ce;'>{date}</span>.</h2>
        </div>
        """
    # Sort events by date ascending
    def event_date(e):
        try:
            return datetime.strptime(e.get('date', ''), '%d-%m-%Y')
        except:
            return datetime.max
    events_sorted = sorted(events, key=event_date)
    html = [f"""
    <div style='font-family:Segoe UI,Roboto,Arial,sans-serif;padding:24px;'>
        <h2 style='color:#222;'>Events for <span style='color:#3182ce;'>{date}</span>:</h2>
        <ul style='font-size:1.1em;padding-left:18px;'>
    """]
    for e in events_sorted:
        date_str = e.get('date', '')
        day_str = e.get('day', '')
        html.append(
            f"<li style='margin-bottom:16px;'>"
            f"<strong style='color:#111;font-size:1.15em;'>{e['event_name']}</strong>"
            f" <span style='color:#555;font-size:0.95em;'><b>(Date: {date_str}{' - ' + day_str if day_str else ''})</b></span>"
            f"{' <span style=\"color:#3182ce;font-weight:500;\">at ' + e.get('time', '') + '</span>' if e.get('time', '') else ''}"
            f"{' <span style=\"color:#555;font-style:italic;\">' + e.get('extra_info', '') + '</span>' if e.get('extra_info', '') and e.get('extra_info', '') != 'None' else ''}"
            f"</li>"
        )
    html.append("</ul></div>")
    return ''.join(html)

def send_scheduled_mail():
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%d-%m-%Y')
    # Load all events
    with open(EVENTS_PATH, 'r', encoding='utf-8') as f:
        events = json.load(f)

    # Helper to check if event is public
    def is_public(e):
        return e.get('public', True)

    # Next day's events
    next_day_events_all = [e for e in events if e['date'] == tomorrow_str]
    next_day_events_public = [e for e in next_day_events_all if is_public(e)]
    html_next_day_public = format_html_email(next_day_events_public, f"Next Day: {tomorrow_str}")
    html_next_day_all = format_html_email(next_day_events_all, f"Next Day: {tomorrow_str}")

    # This week's remaining events
    this_sunday = today + timedelta(days=(6 - today.weekday()))
    this_sunday_str = this_sunday.strftime('%d-%m-%Y')
    def in_this_week_remaining(e):
        try:
            edate = datetime.strptime(e['date'], '%d-%m-%Y')
            return today.date() <= edate.date() <= this_sunday.date()
        except:
            return False
    this_week_events_all = [e for e in events if in_this_week_remaining(e)]
    this_week_events_public = [e for e in this_week_events_all if is_public(e)]
    html_this_week_public = format_html_email(this_week_events_public, f"This Week Remaining: {today.strftime('%d-%m-%Y')} to {this_sunday_str}")
    html_this_week_all = format_html_email(this_week_events_all, f"This Week Remaining: {today.strftime('%d-%m-%Y')} to {this_sunday_str}")

    # Next week's events
    next_monday = this_sunday + timedelta(days=1)
    next_sunday = next_monday + timedelta(days=6)
    next_monday_str = next_monday.strftime('%d-%m-%Y')
    next_sunday_str = next_sunday.strftime('%d-%m-%Y')
    def in_next_week(e):
        try:
            edate = datetime.strptime(e['date'], '%d-%m-%Y')
            return next_monday.date() <= edate.date() <= next_sunday.date()
        except:
            return False
    next_week_events_all = [e for e in events if in_next_week(e)]
    next_week_events_public = [e for e in next_week_events_all if is_public(e)]
    html_next_week_public = format_html_email(next_week_events_public, f"Next Week: {next_monday_str} to {next_sunday_str}")
    html_next_week_all = format_html_email(next_week_events_all, f"Next Week: {next_monday_str} to {next_sunday_str}")

    # Remaining events of this month
    current_month = today.month
    current_year = today.year
    def in_remaining_month(e):
        try:
            edate = datetime.strptime(e['date'], '%d-%m-%Y')
            return edate.year == current_year and edate.month == current_month and edate.date() >= today.date()
        except:
            return False
    remaining_month_events_all = [e for e in events if in_remaining_month(e)]
    remaining_month_events_public = [e for e in remaining_month_events_all if is_public(e)]
    html_remaining_month_public = format_html_email(remaining_month_events_public, f"Remaining Month: {today.strftime('%B %Y')}")
    html_remaining_month_all = format_html_email(remaining_month_events_all, f"Remaining Month: {today.strftime('%B %Y')}")

    disclaimer_html = "<div style='font-size:0.85em;color:#888;margin-top:24px;text-align:center;'>Events may not be 100% accurate.</div>"
    # Combine event sections for recipients (only public events)
    combined_html_public = "".join([
        f"<h2 style='color:#222;'>Next Day ({tomorrow_str})</h2>" + html_next_day_public,
        f"<h2 style='color:#222;'>This Week Remaining ({today.strftime('%d-%m-%Y')} to {this_sunday_str})</h2>" + html_this_week_public,
        f"<h2 style='color:#222;'>Next Week ({next_monday_str} to {next_sunday_str})</h2>" + html_next_week_public,
        f"<h2 style='color:#222;'>Remaining Events for {today.strftime('%B %Y')}</h2>" + html_remaining_month_public,
        disclaimer_html
    ])
    subject_public = f"Your Calendar: Upcoming Public Events ({tomorrow_str}, This Week: {today.strftime('%d-%m-%Y')} to {this_sunday_str}, Next Week: {next_monday_str} to {next_sunday_str}, {today.strftime('%B %Y')})"

    # Combine event sections for MY_EMAIL (all events)
    combined_html_all = "".join([
        f"<h2 style='color:#222;'>Next Day ({tomorrow_str})</h2>" + html_next_day_all,
        f"<h2 style='color:#222;'>This Week Remaining ({today.strftime('%d-%m-%Y')} to {this_sunday_str})</h2>" + html_this_week_all,
        f"<h2 style='color:#222;'>Next Week ({next_monday_str} to {next_sunday_str})</h2>" + html_next_week_all,
        f"<h2 style='color:#222;'>Remaining Events for {today.strftime('%B %Y')}</h2>" + html_remaining_month_all,
        disclaimer_html
    ])
    subject_all = f"Your Calendar: Upcoming Events ({tomorrow_str}, This Week: {today.strftime('%d-%m-%Y')} to {this_sunday_str}, Next Week: {next_monday_str} to {next_sunday_str}, {today.strftime('%B %Y')})"

    # Send one email to all recipients (public events only)
    for recipient in RECIPIENT_EMAILS:
        try:
            msg = EmailMessage()
            msg.set_content("Your email client does not support HTML. Please view in a modern client.")
            msg.add_alternative(combined_html_public, subtype='html')
            msg['Subject'] = subject_public
            msg['From'] = GMAIL_ADDRESS
            msg['To'] = recipient
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
                smtp.send_message(msg)
            print(f"Scheduled public events email sent to {recipient} via Gmail.")
        except Exception as e:
            print(f"Failed to send public events email to {recipient}: {e}")

    # Send one email to MY_EMAIL (all events)
    try:
        msg_myself = EmailMessage()
        msg_myself.set_content("Your email client does not support HTML. Please view in a modern client.")
        msg_myself.add_alternative(combined_html_all, subtype='html')
        msg_myself['Subject'] = subject_all
        msg_myself['From'] = GMAIL_ADDRESS
        msg_myself['To'] = MY_EMAIL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            smtp.send_message(msg_myself)
        print(f"Scheduled all events email sent to {MY_EMAIL} via Gmail.")
        # Delete next_day_events.txt if exists
        next_day_events_file = os.path.join(os.path.dirname(__file__), 'events/next_day_events.txt')
        if os.path.exists(next_day_events_file):
            os.remove(next_day_events_file)
    except Exception as e:
        print(f"Failed to send all events email to {MY_EMAIL}: {e}")

if __name__ == "__main__":
    send_scheduled_mail()