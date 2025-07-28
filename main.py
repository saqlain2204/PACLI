from agents.pa_agent import PersonalAssistantAgent

if __name__ == "__main__":
    agent = PersonalAssistantAgent()
    while True:
        task = input("Enter your task (or 'exit' to quit): ")
        if task.lower() == 'exit':
            break
        output = agent.run(task)
        print("\n✅ Final Output:\n", output)