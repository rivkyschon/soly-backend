import importlib

from soly_chatbot.agents.agent_manager import Agent
from soly_chatbot.agents.agents_service import contains_finish, remove_finish
# from soly_chatbot.agents.stress_level_assessment_agent import StressLevelAssessmentAgent
from soly_chatbot.prompts.prompts import INITIAL_DISTRESS_RELIEF_PROMPT

HIGH_STRESS_LEVEL = 7
InitialDistressReliefPROMPT = INITIAL_DISTRESS_RELIEF_PROMPT
stress_level_assessment_agent = "soly_chatbot.agents.stress_level_assessment_agent"
module = importlib.import_module(stress_level_assessment_agent)


class InitialDistressReliefAgent(Agent):

    # TODO: change the init access to private
    def __init__(self, prompt=INITIAL_DISTRESS_RELIEF_PROMPT) -> None:
        super().__init__()
        self.prompt = str(self.prompt) + prompt

    async def invoke_input(self, user_input: str) -> None:
        """
        This method is called by the user input.
        param: input: str
        """
        res = self.agent_manager.conversation.invoke(user_input)
        if res["response"] == "FINISH":
            self.agent_manager.transition_to(module.StressLevelAssessmentAgent())
            return None
        if contains_finish(res["response"]):
            res["response"] = remove_finish(res["response"])
            self.agent_manager.transition_to(module.StressLevelAssessmentAgent())
        return res["response"]


