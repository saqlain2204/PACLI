from agents.pa_agent import PersonalAssistantAgent
from utils.terminal_utils import print_title, print_prompt, print_success, print_info, print_event
from sort_events_json import sort_events_json

import os
import json

if __name__ == "__main__":
    # Ensure events folder and event_data.json exist
    events_folder = os.path.join(os.path.dirname(__file__), "events")
    os.makedirs(events_folder, exist_ok=True)
    events_file = os.path.join(events_folder, "event_data.json")
    if not os.path.exists(events_file):
        with open(events_file, "w", encoding="utf-8") as f:
            json.dump([], f)

    print_title("""
██████╗   █████╗   ██████╗ ██╗      ██╗
██╔══██╗ ██╔══██╗ ██╔════╝ ██║      ██║
██████╔╝ ███████║ ██║      ██║      ██║
██╔═══╝  ██╔══██║ ██║      ██║      ██║
██║      ██║  ██║ ╚██████╗ ███████╗ ██║
╚═╝      ╚═╝  ╚═╝  ╚═════╝ ╚══════╝ ╚═╝
    """)
    print_success("Welcome to PACLI - Your AI-powered Personal Assistant!\n")
    print_info("Type your task below, or 'exit' to quit.")
    agent = PersonalAssistantAgent()
    
    while True:
        sort_events_json()
        print_prompt("\nHow can I help you today? > ", end="")
        task = input()
        print_success(task)
        if task.lower() == 'exit':
            print_success("Goodbye! Have a productive day with PACLI.")
            break
        output = agent.run(task)
        print_success("\n✅ Final Output:\n")
        print_event(output)