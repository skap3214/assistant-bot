from langchain import LLMMathChain
from langchain.tools import Tool

def math_tool(llm, verbose = True):
    llm_math = LLMMathChain.from_llm(llm, verbose = verbose)
    final_tool = Tool.from_function(
        func=llm_math.run,
        name="Math",
        description="useful for any mathematical calculations",
    )
    return [final_tool]
