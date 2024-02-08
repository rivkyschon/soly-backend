from soly_chatbot.agents.Initial_distress_relief_agent import InitialDistressReliefAgent
from soly_chatbot.agents.agent_manager import AgentManager
from soly_chatbot.agents.feedback_after_exercise import FeedbackAfterExercise

manager = AgentManager(FeedbackAfterExercise())

while True:
    user_input = input()
    res = manager.invoke_input(user_input)
    if res is None:
        res = manager.invoke_input(user_input)
    print(res)
