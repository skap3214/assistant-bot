#Langchain
from langchain.agents.agent_toolkits import FileManagementToolkit
#api key
import os

def file_tools(root_dir = os.getcwd()):
    toolkit = FileManagementToolkit(root_dir=root_dir)
    file_management_list = toolkit.get_tools() # [copy_file, file_delete, file_search, move_file, read_file, write_file, list_directory]
    return file_management_list

