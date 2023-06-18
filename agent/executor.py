'''
Agent: Executor
Purpose: To execute the tasks outlines by the Planner Agent
'''
#Fix weird import bug
import sys
sys.path.append("")

#Base Class
from base import BaseClass, FeedbackDB
from agent.planner import Planner,tools_list

#Langchain
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent

#Additional Browser Tool
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import create_sync_playwright_browser

base = BaseClass()

class Executor:
    #Create agent
    agent = initialize_agent(
        tools=tools_list,
        llm=base.llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        # return_intermediate_steps=True,
        handle_parsing_errors=True,
    )

    def execute_task(self,task:str):
        return self.agent.run({'input':task})
