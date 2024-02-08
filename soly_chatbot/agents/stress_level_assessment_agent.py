from typing import Any

from soly_chatbot.agents.agent import Agent
from soly_chatbot.agents.agents_service import extract_number_of_stress_level
from soly_chatbot.agents.high_stress_level import HighStressLevel
from soly_chatbot.agents.using_resources import UsingResources
from soly_chatbot.agents.sensory_awareness import SensoryAwareness
from soly_chatbot.prompts.prompts import STRESS_LEVEL_ASSESSMENT_PROMPT


class StressLevelAssessmentAgent(Agent):

    # TODO: change the init access to private
    def __init__(self, prompt=STRESS_LEVEL_ASSESSMENT_PROMPT) -> None:
        super().__init__()
        self.prompt = str(self.prompt) + prompt

    async def invoke_input(self, user_input: str) -> float | Any:
        """
        This method is called by the user input.
        param: input: str
        """
        res = self.agent_manager.conversation.invoke(user_input)
        stress_level = extract_number_of_stress_level(res["response"])
        if stress_level is None:
            return res["response"]
        elif stress_level >= 7:
            self.agent_manager.transition_to(HighStressLevel())
        elif stress_level < 4:
            self.agent_manager.transition_to(UsingResources())
        elif stress_level >= 4:
            self.agent_manager.transition_to(SensoryAwareness())
