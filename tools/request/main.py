from langchain.agents import load_tools

requests_tools = load_tools(["requests_all"])

def request_tools():
    return requests_tools