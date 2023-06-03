#Langchain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
#supabase
import supabase
#api keys
from decouple import config
import os
os.environ['OPENAI_API_KEY'] = config('OPENAI')

class BaseClass():
    '''
    Add any base Langchain/External Lib classes needed throughout the project here
    as a var.
    Connects to Supabase as well
    #TODO: User Auth in constructor and RLS to be modified when repo is public!!
    Some more 'UI' features for better terminal output for debugging
    ### Variables
    - llm: language model used (GPT 3.5 Turbo)
    - embeddings : enbeddings used (OpenAI)
    - supabase : to access supabase database
    - RESET : to reset the terminal output color back to default
    - COLORS [R,G,Y,B,P,C,W] : output color when you want to print something out,
                            append the color before the string and postfix the string with RESET 
    '''
    #ANSI escape seqs for multi color output
    #Always append reset to output string to reset color of output in the end
    RESET = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    #langchain stuff
    llm = ChatOpenAI(temperature=0)
    embeddings = OpenAIEmbeddings()
    #db
    supabase = supabase.create_client(config('SUPABASE_URL'), config('SUPABASE_KEY'))

    def insert_history(self,data : dict):
        try:
            response = self.supabase.table("history").insert(data).execute()
            return response
        except Exception as e:
            return e

    def delete_history(self,record_id : int):
        try:
            response = self.supabase.table("history").delete().eq("id", record_id).execute()
            return response
        except Exception as e:
            return e

    def update_history(self,record_id : int, data : dict):
        try:
            response = self.supabase.table("history").update(data).eq("id", record_id).execute()
            return response
        except Exception as e:
            return e
    
    def add_history(self,output):
        '''
        Add all details to the supabase db
        #TODO: based on type of output, parse and add output accordingly
        '''
        pass
    
    def get_all_history(self):
        '''
        returns the full history table
        '''
        try:
            response = self.supabase.table('history').select("*").execute()
            return response.data
        except Exception as e:
            return e

