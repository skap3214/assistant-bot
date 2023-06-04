#Fix weird import error
import sys
sys.path.append('')

#Base Class
from base import BaseClass

#Langchain
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.agents.tools import Tool
from langchain.agents import initialize_agent, AgentType

#api key
import os

toolkit = FileManagementToolkit()
file_management_list = toolkit.get_tools() # [copy_file, file_delete, file_search, move_file, read_file, write_file, list_directory]
copy_file, file_delete, file_search, move_file, read_file, write_file, list_directory = file_management_list
print(copy_file)
def file_tools(root_dir = os.getcwd()):
    toolkit = FileManagementToolkit(root_dir=root_dir)
    file_management_list = toolkit.get_tools() # [copy_file, file_delete, file_search, move_file, read_file, write_file, list_directory]
    return file_management_list

def copy_file_run(string):
    source_path, destination_path = string.split(",")
    output = copy_file._run(source_path, destination_path)
    return output

tool = Tool.from_function(
    name="copy_file",
    func=copy_file_run,
    description='''Create a copy of a file in a specified location.
    The input to this tool should be a comma separated list of strings of length two, 
    representing the source path and the destination path, respectively'''

)

agent = initialize_agent(
    [tool], BaseClass.llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose = True
)

agent.run('copy main.py in my current dir and name the copied file test.py')


