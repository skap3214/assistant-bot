#Fix weird import bug
import sys
sys.path.append("")

#Base Class
from base import BaseClass

#Agent Class
from tools.main import CustomAgent



agent = CustomAgent()#Name does not update currently
agent.initiate_agent(verbose=True, incognito=True, tts=True)
while True:
    query = input(f"\nAsk a question to {agent.name}\n")
    print(agent.ask(query)[0]['response'])