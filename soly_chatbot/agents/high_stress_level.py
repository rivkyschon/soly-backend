from soly_chatbot.agents.agent_manager import Agent
from soly_chatbot.agents.feedback_after_exercise import FeedbackAfterExercise
from soly_chatbot.appendices.exercises import EXERCISES_FOR_HIGH_STRESS_LEVEL
from soly_chatbot.prompts.prompts import HIGH_STRESS_LEVEL_PROMPT


class HighStressLevel(Agent):
    def __init__(self, prompt=HIGH_STRESS_LEVEL_PROMPT) -> None:
        super().__init__()
        self.prompt = prompt
        self.exercises = EXERCISES_FOR_HIGH_STRESS_LEVEL

    async def invoke_input(self, user_input: str) -> None | str:
        res = self.agent_manager.conversation.invoke(user_input)
        if res["response"] == "FINISH":
            self.agent_manager.transition_to(FeedbackAfterExercise())
            return None
        res["response"] = self.append_exercise_detail(res["response"])
        return res["response"]

    def append_exercise_detail(self, bot_response):
        for exercise in self.exercises:
            if exercise in bot_response:
                return bot_response + f" {{{self.exercises[exercise]}}}"
        return bot_response
