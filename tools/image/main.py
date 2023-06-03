from langchain.agents import load_tools

import os
from decouple import config
os.environ["SCENEX_API_KEY"] = config('SCENEXPLAIN')

tools = load_tools(["sceneXplain"])
def image_tool():
    return tools
