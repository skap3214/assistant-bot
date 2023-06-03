from langchain.tools import HumanInputRun
from langchain.agents import load_tools
def human_tool():
    return load_tools(['human'])
