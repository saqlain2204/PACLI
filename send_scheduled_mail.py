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
    html = [f"""
    <div style='font-family:Segoe UI,Roboto,Arial,sans-serif;padding:24px;'>
        <h2 style='color:#222;'>Events for <span style='color:#3182ce;'>{date}</span>:</h2>
        <ul style='font-size:1.1em;padding-left:18px;'>
    """]
    for e in events:
        html.append(
            f"<li style='margin-bottom:16px;'>"
            f"<strong style='color:#111;font-size:1.15em;'>{e['event_name']}</strong>"
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
    # Load events for tomorrow
    with open(EVENTS_PATH, 'r', encoding='utf-8') as f:
        events = json.load(f)
    next_day_events = [e for e in events if e['date'] == tomorrow_str]

    html_message = format_html_email(next_day_events, tomorrow_str)

    # Send to all recipients in RECIPIENT_EMAILS
    for recipient in RECIPIENT_EMAILS:
        try:
            msg = EmailMessage()
            msg.set_content("Your email client does not support HTML. Please view in a modern client.")
            msg.add_alternative(html_message, subtype='html')
            msg['Subject'] = f'Your Calendar: Events for {tomorrow_str}'
            msg['From'] = GMAIL_ADDRESS
            msg['To'] = recipient
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
                smtp.send_message(msg)
            print(f"Scheduled email sent to {recipient} via Gmail.")
        except Exception as e:
            print(f"Failed to send scheduled email to {recipient}: {e}")

    # Send all events to MY_EMAIL
    try:
        msg_myself = EmailMessage()
        msg_myself.set_content("Your email client does not support HTML. Please view in a modern client.")
        msg_myself.add_alternative(html_message, subtype='html')
        msg_myself['Subject'] = f'Your Calendar: All Events for {tomorrow_str}'
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