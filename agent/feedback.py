'''
Agent: Feedback
Purpose: To provide/update feedback/critique on the most recent converstation
Input Vars: recent_chat_history, feedback
'''
#Fix weird import bug
import sys
sys.path.append("")

#Langchain
from langchain.agents import initialize_agent
from langchain import PromptTemplate, LLMChain

#Base Class
from base import BaseClass, FeedbackDB

base = BaseClass()
f_db = FeedbackDB()



class FeedbackAgent:

    base_template = '''You are Feedback Agent. You are a master critic whos job is to provide 
    very accurate, and helpful feedback to another Agent called Planner. The Planner Agent is responsible for planning out actions that in the end will
    solve problems and do tasks for the user. Your job as the Feedback Agent is to update/provider feedback in a manner that helps the Planner Agent to plan out tasks and steps more efficiently and error free.
    The goal of the Planner agent is to effectively, efficiently create steps to answer, solve the users' questions.
    You will provide this feedback based on the most current user interaction with the Agent and the previous feedback.
    The user interaction consists of input from the user, steps taken by an Executor Agent, and output.
    Here is the user interaction:
    {chat_history}

    Here is the current feedback given by you(Feedback Agent):
    {feedback}

    If you think the current feedback is sufficient output the current feedback.
    Directly Address your prompt to the Planner Agent. Do not add the words 'Executor Agent', 'Planner Agent', instead say 'You'. 
    Do not comment directly on previous interactions, use them as context to create better feedback for the Planner Agent.
    Remember, the feedback you will output now will replace the current feedback above and will be given to the Planner Agent for future interactions.
    Updated feedback:
    '''

    #Create the Feedback Chain using the prompt
    feedback_prompt = PromptTemplate(
        input_variables=['chat_history', 'feedback'],
        template=base_template,
    )
    feedback_chain = LLMChain(
        llm = base.llm,
        prompt=feedback_prompt,
        verbose=True
    )

    def update_feedback(self,data : dict):
        '''
        Update feedback in DB using feedback llm chain.
        Returns the feedback returned by the feedback chain
        '''
        #Convert chat_history to better format
        user = data['message']
        agent = data['response']
        steps = data['verbose']
        interaction = f"""User: {user}
        steps_taken: {steps}
        Executor: {agent}
        """
            
        #Get most recent feeedback from DB
        feedback = self.get_feedback()

        #Query feedback chain
        query = {
            'chat_history' : data,
            'feedback' : feedback,
        }
        new_feedback = self.feedback_chain(query)

        #Update feedback to DB
        query['feedback'] = new_feedback
        f_db.insert_feedback(query)

        return new_feedback
    
    def get_feedback(self):
        return f_db.get_most_recent()[0]['feedback']







