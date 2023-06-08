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
from langchain.agents import initialize_agent, ConversationalChatAgent
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
from tools.request.main import request_tools
from tools.spotify.main import add_song_tool
# from tools.gradio.main import gradio_tools

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
        self.prompt = '''Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.'''
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
                request_tools() +
                add_song_tool()
            )

        else:
            self.tools_list = tools
        
        print(f"Adding selected tools to {self.name} 50%")
        #Create the agent
        print("Trying to combine everything!")
        self.agent = initialize_agent(
            self.tools_list, 
            self.llm, 
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
            verbose=verbose, 
            memory=self.memory,
            agent_kwargs={"PREFIX" : self.prompt})
        print(f"{self.base.PURPLE}{self.name} is now active and ready to assist you! {self.base.RESET}")
        self.init = True
    
    def ask(self,query):
        if not self.init:
            print(f"You have not initiated {self.name}. Please run the 'initiate_agent()' method")
            return 0
        if self.incognito:
            #TODO: do not chat history data to db
            pass
        else:
            return self.agent.run(input=query)


#Code to test agent
agent = CustomAgent()
agent.initiate_agent(verbose=True)
while True:
    query = input(f"\nAsk a question to {agent.name}\n")
    print(agent.ask(query))