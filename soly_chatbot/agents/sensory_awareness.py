import time
from soly_chatbot.agents.agent_manager import Agent
from soly_chatbot.agents.using_resources import UsingResources
from soly_chatbot.prompts.prompts import SensoryAwarenessPROMPT
from soly_chatbot.agents.agents_service import is_finished

SensoryAwarenessPROMPT = SensoryAwarenessPROMPT

END_OF_STATEMENT = 'FINISH'
SECONDS_TO_FINISH = 180


def time_finished(start_time):
    # Check if the time that assigned has passed
    return (time.time() - start_time) >= SECONDS_TO_FINISH


class SensoryAwareness(Agent):
    def __init__(self, prompt=SensoryAwarenessPROMPT) -> None:
        super().__init__()
        self.prompt = str(self.prompt) + prompt
        self.start_time = None

    async def invoke_input(self, user_input: str) -> str | None:
        """
        This method is called by the user input.
        param: input: str
        """
        # Initialize start_time when the method is called for the first time
        if self.start_time is None:
            self.start_time = time.time()

        res = self.agent_manager.conversation.invoke(user_input)
        print(res['response'])

        # Check if the response is FINISH or if the time that assigned has passed
        if is_finished(END_OF_STATEMENT, res['response']) or time_finished(self.start_time):
            self.agent_manager.transition_to(UsingResources())
            self.start_time = None  # Reset the start time for the next invocation
            return None

        return res["response"]
