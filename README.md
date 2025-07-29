# PACLI

A powerful, AI-driven personal assistant for your calendar, scheduling, and event management. Built with LangChain, Groq LLM, and a flexible tool system, PACLI helps you manage your schedule, add and edit events, and answer natural language queries about your calendar—all from the command line.

## Features
- **Natural Language Scheduling:** Add events using plain English (e.g., "Schedule OA next Tuesday at 5pm").
- **Flexible Event Retrieval:** Ask for events in any time range ("next week", "next 2 weeks", "next 5 days", etc.).
- **Event Editing:** Edit or update events by name and date.
- **Event Search:** Find events by name and date, even with fuzzy matching.
- **Persistent Storage:** All events are stored in local JSON files for reliability and privacy.
- **Autonomous Tool Calling:** The agent automatically selects and calls the right tool for your query.
- **Customizable Prompts:** Easily update assistant instructions via the YAML prompt file.
- **Colorful CLI Output:** Enjoy a clear, readable interface with rich formatting.
- **Codeforces Contest Integration:** Query upcoming Codeforces contests, schedule them to your calendar, and get contest details for any date or time range using natural language (e.g., "Show Codeforces contests next week").
- **Automated Next-Day Event Email:** Get a beautiful HTML email of your next day's events sent automatically via Gmail.

## Automated Next-Day Event Email

1. Schedule `send_scheduled_mail.py` with Windows Task Scheduler to send the email at your preferred time.
2. The email uses HTML formatting for a clear, modern look.
3. After sending, the events file is deleted for privacy.

**Setup:**
- Add your Gmail credentials and recipient email to `.env` (use an App Password if 2FA is enabled).
- Make sure `python-dotenv` is installed (`pip install python-dotenv`).
- Use the real Python executable path in Task Scheduler (not the Windows Store launcher).


**Note:**
- Your confidential data stays local; no event info is sent to external servers except Gmail.
- **Docker support is currently not added for email automation or the calendar/frontend.**
- To use the calendar UI (frontend), run it locally and fetch event data directly from the backend. You can schedule and interact with the frontend and email/calendar automation using Windows Task Scheduler or by running the scripts manually. See below for instructions.

## Usage

### 1. Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/saqlain2204/PACLI.git
   cd PACLI
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set up your environment:**
    Create `.env` and add your Groq API key and Gmail credentials:
     ```env
     GROQ_API_KEY=your_groq_api_key_here
     GMAIL_ADDRESS=your_gmail_address@gmail.com
     GMAIL_APP_PASSWORD=your_gmail_app_password
     RECIPIENT_EMAIL=recipient_email@gmail.com
     ```

### 2. Running the Assistant

#### Run with Python (local)
```sh
python main.py
```

You'll see:
```
How can i help you today? >
```
Type your query, such as:
- `Schedule OA next Wednesday at 10am`
- `What events do I have next week?`
- `Edit Interviews on 09-08-2025, set time to 9:30 AM`
- `Find OA on 05-08-2025`

### 3. Event Data
- Events are stored in `events/event_data.json` (excluded from git by default).
- The assistant supports date formats like `DD-MM-YYYY` and natural language ("next Friday").

### 4. Customizing Prompts
- Edit `prompts/personal_assistant.yaml` to change the assistant's instructions or logic.
- No code changes needed—just update the YAML file.

### 5. Adding/Editing Tools
- Tools are defined in the `tools/` folder.
- Add new tools or update existing ones to extend functionality.

## Project Structure
```
Personal Assistant/
├── agents/
│   └── pa_agent.py
├── tools/
│   ├── event_scheduler.py
│   ├── get_events.py
│   ├── edit_event_tool.py
│   ├── find_event_tool.py
│   └── ...
├── prompts/
│   └── personal_assistant.yaml
├── events/
│   └── event_data.json
├── main.py
├── send_scheduled_mail.py
├── README.md
└── requirements.txt
```

## Advanced Usage
- The assistant supports flexible queries and autonomous tool selection.
- You can extend the agent with new tools, prompts, or UI (e.g., Streamlit).

## License
MIT

## Author
Mohammed Saqlain

---
Enjoy PACLI, your AI-powered personal assistant! If you have questions or want to contribute, open an issue or pull request.
