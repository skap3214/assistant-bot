#Fix weird import bug
import sys
sys.path.append("")

from agent.executor import Executor
from agent.feedback import FeedbackAgent
from agent.planner import Planner

from base import BaseClass

class LearningAgent:
    '''
    Ask for user input
    plan out task
    execute task
    return result from executor
    get feedback from feedback agent
    '''
    planner_agent = Planner()
    feedback_agent = FeedbackAgent()
    execute_agent = Executor()

    def run(self,query:str):
        get_plan = self.planner_agent.plan(query)
        print(get_plan)
        print()
        output = self.execute_agent.execute_task(get_plan)
        return output

#Test
agent = LearningAgent()
while True:
    task = input("Ask me a question:\n")
    print(agent.run())