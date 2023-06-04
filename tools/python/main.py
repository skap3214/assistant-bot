from langchain.agents import Tool
from langchain.utilities import PythonREPL

python_repl = PythonREPL()

repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. The python command cannot be more than one line long. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run
)

def python_tool():
    return [repl_tool]