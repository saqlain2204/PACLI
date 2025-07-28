from agents.pa_agent import PersonalAssistantAgent
from utils.terminal_utils import print_title, print_prompt, print_success, print_info

if __name__ == "__main__":
    print_title("""
██████╗  █████╗  ██████╗██╗     ██╗
██╔══██╗██╔══██╗██╔════╝██║     ██║
██████╔╝███████║██║     ██║     ██║
██╔═══╝ ██╔══██║██║     ██║     ██║
██║     ██║  ██║╚██████╗███████╗██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝
""")
    print_success("Welcome to PACLI - Your AI-powered Personal Assistant!\n")
    print_info("Type your task below, or 'exit' to quit.")
    agent = PersonalAssistantAgent()
    while True:
        print_prompt("\nAsk or Add Anything:")
        task = input()
        if task.lower() == 'exit':
            print_success("Goodbye! Have a productive day with PACLI.")
            break
        output = agent.run(task)
        print_success("\n✅ Final Output:\n")
        print(output)