import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools.event_scheduler import schedule_event
from tools.get_events import get_event_schedule
from tools.edit_event_tool import edit_event
from tools.find_event_tool import find_event

class PersonalAssistantAgent:
    def __init__(self):
        load_dotenv()
        self.llm = ChatGroq(model_name="llama3-70b-8192", temperature=0)

        now = datetime.now()
        current_day = now.strftime("%A")
        current_date = now.day
        current_month = now.strftime("%B")
        current_year = now.year

        # Load system prompt from prompts/personal_assistant.yaml
        import yaml
        prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "personal_assistant.yaml")
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompts = yaml.safe_load(f)
        system_prompt = prompts["system"]
        # Format system prompt with current date context
        system_prompt = system_prompt.format(
            current_day=current_day,
            current_month=current_month,
            current_date=current_date,
            current_year=current_year
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        self.tools = [get_event_schedule, schedule_event, edit_event, find_event]
        self.agent = create_tool_calling_agent(llm=self.llm, tools=self.tools, prompt=self.prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def run(self, user_input: str) -> str:
        result = self.agent_executor.invoke({"input": user_input})
        return result["output"]