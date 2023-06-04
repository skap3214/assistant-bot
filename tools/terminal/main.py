#Fix weird import error
import sys
sys.path.append('')

#Base Class
from base import BaseClass

#Langchain
from langchain.tools import ShellTool

shell_tool = ShellTool()
shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace("{", "{{").replace("}", "}}")

def terminal_tool():
    return [shell_tool]