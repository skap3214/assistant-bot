'''
Agent: Planner
Purpose: The plan out the steps and tools the executor agent will need to do
Input Vars: chat_history, feedback, tools
'''
#Fix weird import bug
import sys
sys.path.append("")

#Langchain
from langchain.agents import initialize_agent
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationTokenBufferMemory

#Base Class
from base import BaseClass, FeedbackDB
from agent.feedback import FeedbackAgent

#Tools
from tools.search.main import search_tool
# from tools.file_management.main import file_tools
from tools.math.main import math_tool
from tools.image.main import image_tool
from tools.human.main import human_tool
from tools.terminal.main import terminal_tool
from tools.arxiv.main import arxiv_tool
from tools.python.main import python_tool
from tools.request.main import request_tools
from tools.spotify.main import add_song_tool
from tools.google_drive.main import add_to_google_drive_tool
from tools.elevenlabs.main import convert_text_to_speech
from tools.call_my_device.main import find_my_device_tool
# from tools.gradio.main import gradio_tools

base = BaseClass()
feedback_agent = FeedbackAgent()
f_db = FeedbackDB


planner_template = """You are the Planner Agent. You are a master planner who excels at breaking down complex tasks into a series of steps.
Your job is to provide a step by step solution to a task given by the user. Your goal is to provide an efficient, elegant, error-free plan in the form of a list of steps.
The user can ask you a wide asssortment of tasks, randing from easy to complex. Your plan will be given to an Executor Agent, which will execute all the steps you outline it.
The Executor does NOT have access to the chat_history so you will have to give stesp accordingly.
The Executor Agent has access to these tools to help execute the steps you outline:
{tools_list}

Generate the steps keeping the tools in mind.
Here are the previous interactions you have had with the user. If needed, use this as context:
{chat_history}

Here are some helpful guidelines to keep in mind:
{feedback}

This is the user input:
{input}

Assistant:
"""
tools_list = []
tools_list.extend(search_tool() +
    math_tool(base.llm) +
    image_tool() +
    human_tool() +
    terminal_tool() +
    arxiv_tool() +
    python_tool() +
    request_tools() +
    add_song_tool() +
    add_to_google_drive_tool() +
    find_my_device_tool()
)

#Create tools string to give prompt
tool_strings = "\n".join(
    [f"> {tool.name}: {tool.description}" for tool in tools_list]
)

#Create prompt and add in variables partially
planner_prompt = PromptTemplate(
    input_variables=['tools_list', 'chat_history', 'feedback', 'input'],
    template=planner_template,
)
planner_prompt = planner_prompt.partial(
    feedback = feedback_agent.get_feedback(),
    tools_list = tool_strings,
)

class Planner:
    memory = ConversationTokenBufferMemory(llm=base.llm, return_messages=True, memory_key='chat_history',human_prefix='user', input_key='input', max_token_limit=2100)
    history = base.get_all_history()
    for row in history:
            message = row['message']
            output = row['response']
            #Add message, output to agent memory
            memory.save_context({"input":message},{"output":output})

    # Create planner chain
    planner_chain = LLMChain(
          llm=base.llm,
          prompt=planner_prompt,
          verbose=True,
          memory=memory,
    )

#Test
plan = Planner()
output = plan.planner_chain.predict(
      input="What is the weather going to be like tomorrow in Chennai,India?"
)
print(output)