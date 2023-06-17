'''
Main file for merging all tools. The tools will be then added to an agent.
'''
#Fix weird import error
import sys
sys.path.append('')

#Base Class
from base import BaseClass

#Langchain
from langchain.agents import initialize_agent, ConversationalChatAgent
from langchain.agents import AgentType
from langchain.experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner

#Memory
from langchain.memory import ConversationTokenBufferMemory

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

#formatting
import json

#api keys
from decouple import config
import os
os.environ['OPENAI_API_KEY'] = config('OPENAI')

class CustomAgent():
    def __init__(self, base = BaseClass, name="Assistant"):
        self.name = name
        self.base = base
        self.llm = self.base.llm
        self.init = False
        self.tools_list = []
        self.incognito = False
        self.agent = False
        self.tts = False
        self.prompt = f'''Your name is {self.name}. {self.name} is a large language model trained by OpenAI.

{self.name} is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, {self.name} is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

{self.name} is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, {self.name} is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, {self.name} is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, {self.name} is here to assist.'''
        self.memory = ConversationTokenBufferMemory(llm=self.llm, return_messages=True, ai_prefix=name, memory_key="chat_history", output_key='output')
        print(f"{self.base.BLUE} {self.name} is ready to be initiated, now on standby {self.base.RESET}")
    
    def add_memory(self,memory):
        if not self.init:
            self.memory = memory
        else:
            print("Cannot change memory once agent is initiated")
            return 0
    
    def get_long_term_memory(self):
        history = self.base.get_all_history(self.base)
        for row in history:
            input = row['message']
            output = row['response']
            #Add input, output to agent memory
            self.memory.save_context({"input":input},{"output":output})
        print(f"{self.base.YELLOW}Long Term Memory added {self.base.RESET}")
    def initiate_agent(
            self,
            verbose = True, 
            incognito = False, 
            debug = True, 
            tools = "all",
            long_term_memory = True,
            tts=False,
            type="CRD"):
        
        #Incognito
        print(f"{self.base.PURPLE} Creating {self.name} 0% {self.base.RESET}")
        self.incognito = incognito
        if incognito:
            print(f"{self.base.GREEN} Incognito On. Session memory will not be saved long-term {self.base.RESET} (NOTE: Only supported option currently, will default to incognito until db is setup)")
        
        #Add Tools to self.tools_list
        if tools == "all":
            self.tools_list.extend(
                search_tool() +
                math_tool(self.llm) +
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

        else:
            self.tools_list = tools
        print(f"Adding selected tools to {self.name} 50%")

        #Memory
        if long_term_memory:
            self.get_long_term_memory()
        
        #Create the agent
        print("Trying to combine everything!")
        if type == "CRD":
            self.agent = initialize_agent(
                self.tools_list, 
                self.llm, 
                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, 
                verbose=verbose, 
                return_intermediate_steps=True,
                memory=self.memory,
                handle_parsing_errors=True,
                agent_kwargs={"prefix" : self.prompt, "ai_prefix" : self.name}
                )
        elif type == "PAE":
            self.executor = load_agent_executor(self.base.llm, self.tools_list, verbose=True)
            self.planner = load_chat_planner(self.base.llm)
            self.agent = PlanAndExecute(memory=self.memory,planner=self.planner, executer=self.executor, verbose=True)
        else:
            print("Unknown agent type, please choose between CRD or PAE")
            return 0
        self.tts = tts
        print(f"{self.base.PURPLE}{self.name} is now active and ready to assist you! {self.base.RESET}")
        self.init = True
    
    def ask(self,query):
        if not self.init:
            print(f"You have not initiated {self.name}. Please run the 'initiate_agent()' method")
            return 0
        
        response = self.agent({"input":query})
        intermediate_steps = response['intermediate_steps']
        data = {
                'message' : query,
                'response' : response['output'],
                'verbose' : intermediate_steps
            }
        db_query = None
        if not self.incognito:
            data = {
                'message' : query,
                'response' : response['output'],
                'verbose' : intermediate_steps
            }
            db_query = self.base.insert_history(self.base,data)
        
        if self.tts:
            convert_text_to_speech(response['output'])

        return data,db_query

