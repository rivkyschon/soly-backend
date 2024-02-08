from db_management.entities_CRUD.resource_CRUD import get_all_resources
from soly_chatbot.agents.agent import Agent
from soly_chatbot.prompts.prompts import USING_RESOURCES_PROMPT


class UsingResources(Agent):
    def __init__(self, prompt=USING_RESOURCES_PROMPT) -> None:
        super().__init__()
        self.prompt = str(self.prompt) + prompt

    async def invoke_input(self, user_input: str) -> str | None:
        resources = await self.get_resources()
        self.prompt = self.prompt + "List of experiences" + str(resources)
        res = self.agent_manager.conversation.invoke(user_input)
        return res["response"]

    async def get_resources(self):
        return await get_all_resources(self.agent_manager.user_id)