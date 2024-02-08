import re

from soly_chatbot.agents import stress_level_assessment_agent
from soly_chatbot.agents.agent import Agent
import importlib

from soly_chatbot.agents.agents_service import contains_finish, remove_finish
from soly_chatbot.prompts.prompts import FEEDBACK_AFTER_EXERCISE_PROMPT

Stress_level_assessment_agent = "soly_chatbot.agents.stress_level_assessment_agent"
module = importlib.import_module(Stress_level_assessment_agent)


class FeedbackAfterExercise(Agent):
    def __init__(self) -> None:
        super().__init__()
        self.prompt = str(self.prompt) + FEEDBACK_AFTER_EXERCISE_PROMPT

    async def invoke_input(self, user_input: str) -> None:
        res = self.agent_manager.conversation.invoke(user_input)

        if res["response"] == "FINISH":
            self.agent_manager.transition_to(module.StressLevelAssessmentAgent())
            return None
        if contains_finish(res["response"]):
            res["response"] = remove_finish(res["response"])
            self.agent_manager.transition_to(module.StressLevelAssessmentAgent())
        return res["response"]

        # initial_stress_level_pattern = r'\bINITIAL_STRESS_LEVEL\b'
        # exercise_pattern = r'\bEXERCISE\b'
        #
        # initial_stress_level_match = bool(re.search(initial_stress_level_pattern, res['response']))
        # exercise_match = bool(re.search(exercise_pattern, res['response']))
        # initial_distress_relief_agent = module.InitialDistressReliefAgent()
        # if initial_stress_level_match:
        #     self.agent_manager.transition_to(initial_distress_relief_agent)
        # elif exercise_match:
        #     self.agent_manager.transition_to(initial_distress_relief_agent)
        # else:
        #     return res['response']
        # return None
