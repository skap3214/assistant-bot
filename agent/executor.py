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
from langchain.agents import initialize_agent, StructuredChatAgent

#Additional Browser Tool
from langchain.agents.agent_toolkits import PlayWrightBrowserToolkit
from langchain.tools.playwright.utils import create_sync_playwright_browser

base = BaseClass()

#Default prompts for the agent
# flake8: noqa
PREFIX = """You are the Executor Agent. You are proficient at executing tasks give to you in a step by step manner.
The instructions given to you will be step by step instructions which you will need to execute one by one, EXACTLY as it has been given to you.
The instructions given to you are by the Planner Agent and together you both have to assist the user in any tasks or questions the user gives to you.
 You have access to the following tools:"""
FORMAT_INSTRUCTIONS = """Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

```
{{{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}}}
```

Follow this format:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}}}
```"""
SUFFIX = """Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.
Thought:"""

class Executor:
    #Create agent
    agent = initialize_agent(
        tools=tools_list,
        llm=base.llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        # return_intermediate_steps=True,
        handle_parsing_errors=True,
        agent_kwargs={
            'prefix' : PREFIX,
            'suffix' : SUFFIX,
            'format_instructions' : FORMAT_INSTRUCTIONS,
        }
    )

    def execute_task(self,task:str):
        return self.agent.run({'input':task})
