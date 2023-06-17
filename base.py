#Langchain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
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
    # llm_nonchat = OpenAI(temperature=0, model_name="gpt-3.5-turbo")
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
    
    def get_all_history(self,query="*"):
        '''
        returns the full history table
        '''
        try:
            response = self.supabase.table('history').select(query).execute()
            return response.data
        except Exception as e:
            return e

class FeedbackDB():

    supabase = supabase.create_client(config('SUPABASE_URL'), config('SUPABASE_KEY'))

    def insert_feedback(self,data : dict):
        try:
            response = self.supabase.table("feedback").insert(data).execute()
            return response
        except Exception as e:
            return e

    def delete_feedback(self,record_id : int):
        try:
            response = self.supabase.table("feedback").delete().eq("id", record_id).execute()
            return response
        except Exception as e:
            return e

    def update_feedback(self,record_id : int, data : dict):
        try:
            response = self.supabase.table("feedback").update(data).eq("id", record_id).execute()
            return response
        except Exception as e:
            return e
    
    def get_all_feedback(self,query="*"):
        '''
        returns the full feedback table
        '''
        try:
            response = self.supabase.table('feedback').select(query).execute()
            return response
        except Exception as e:
            return e
    
    def get_most_recent(self):
        try:
            response = self.supabase.table('feedback').select('*').order('created_at', desc=True).limit(1).execute()
            return response.data
        except Exception as e:
            return e