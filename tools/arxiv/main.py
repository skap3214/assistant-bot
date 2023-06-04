from langchain.agents import load_tools

arxiv_tool_langcain = load_tools(['arxiv'])

def arxiv_tool():
    return arxiv_tool_langcain