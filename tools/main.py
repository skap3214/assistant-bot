'''
Main file for merging all tools. The tools will be then added to an agent.
'''
#Fix weird import error
import sys
sys.path.append('')

#Base Class
from base import BaseClass

#Langchain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

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
from tools.gradio.main import gradio_tools

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
        self.memory = ConversationTokenBufferMemory(llm=self.llm, return_messages=True, ai_prefix=name, memory_key="chat_history")
        print(f"{self.base.BLUE} {self.name} is ready to be initiated, now on standby {self.base.RESET}")
    
    def add_memory(self,memory):
        if not self.init:
            self.memory = memory
        else:
            print("Cannot change memory once agent is initiated")
            return 0
    def initiate_agent(self,verbose = True, incognito = False, debug = True, tools = "all"):
        #If you do not want to save this sessions chat history(previous chat will still be there)
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
                gradio_tools()
            )
                                    
            
        else:
            self.tools_list = tools
        
        print(f"Adding selected tools to {self.name} 50%")
        #Create the agent
        print("Trying to combine everything!")
        self.agent = initialize_agent(self.tools_list, self.llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=verbose, memory=self.memory)
        print(f"{self.base.PURPLE} {self.name} is now active and ready to assist you! {self.base.RESET}")
        self.init = True
    
    def ask(self,query):
        if not self.init:
            print(f"You have not initiated {self.name}. Please run the 'initiate_agent()' method")
            return 0
        if self.incognito:
            #TODO: do not chat history data to db
            pass
        else:
            self.agent.run(input=query)


#Code to test agent
agent = CustomAgent(name="Bob")
agent.initiate_agent()
while True:
    query = input(f"Ask a question to {agent.name} ")
    agent.ask(query)