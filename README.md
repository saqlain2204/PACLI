
# PACLI

A powerful, AI-driven personal assistant for your calendar, scheduling, and event management. Built with LangChain, Groq LLM, and a flexible tool system, PACLI helps you manage your schedule, add and edit events, and answer natural language queries about your calendar—all from the command line.

## Features
- **Natural Language Scheduling:** Add events using plain English (e.g., "Schedule Flipkart OA next Tuesday at 5pm").
- **Flexible Event Retrieval:** Ask for events in any time range ("next week", "next 2 weeks", "next 5 days", etc.).
- **Event Editing:** Edit or update events by name and date.
- **Event Search:** Find events by name and date, even with fuzzy matching.
- **Persistent Storage:** All events are stored in local JSON files for reliability and privacy.
- **Autonomous Tool Calling:** The agent automatically selects and calls the right tool for your query.
- **Customizable Prompts:** Easily update assistant instructions via the YAML prompt file.
- **Colorful CLI Output:** Enjoy a clear, readable interface with rich formatting.

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
    Create `.env` and add your Groq API key:
     ```env
     GROQ_API_KEY=your_groq_api_key_here
     ```


### 2. Running the Assistant

#### Run with Python (local)
```sh
python main.py
```

#### Run with Docker
Build the image:
```sh
docker build -t pacli .
```
Run the container (pass your Groq API key):
```sh
docker run --env GROQ_API_KEY=your_groq_api_key_here -it pacli
```

You'll see:
```
Enter your task (or 'exit' to quit):
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
├── README.md
└── requirements.txt
```

## Advanced Usage
- The assistant supports flexible queries and autonomous tool selection.
- You can extend the agent with new tools, prompts, or UI (e.g., Streamlit).

## License
MIT

## Author
Saqlain (and GitHub Copilot)

---
Enjoy PACLI, your AI-powered personal assistant! If you have questions or want to contribute, open an issue or pull request.
