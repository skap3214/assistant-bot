#langchain
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import Tool


def search_tool():
    search = DuckDuckGoSearchRun()
    return [search]

