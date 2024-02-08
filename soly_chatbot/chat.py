import re

from db_management.models.entities import Message, User
from soly_chatbot.agents.Initial_distress_relief_agent import InitialDistressReliefAgent
from soly_chatbot.agents.agent_manager import AgentManager


class Chat:
    def __init__(self, conversation_id: str, user_id: str):
        self.conversation_id = conversation_id
        self.user_id = user_id
        self.agent_manager = AgentManager(InitialDistressReliefAgent(), self.user_id)

    async def get_response(self, user_input) -> Message:
        res = await self.agent_manager.invoke_input(user_input)
        if res is None:
            res = await self.agent_manager.invoke_input(user_input)
        # Convert the response to a Message object
        attachment, res = self.extract_and_remove_attachment(res)
        res_message = Message(conversation_id=self.conversation_id, content=res, attachment=attachment)

        # Serialize the Message object to JSON without escaping Unicode characters
        return res_message

    def extract_and_remove_attachment(self, s: str) -> (str, str):
        # Regular expression to match '{value}' at the end of the string
        pattern = r'\{([^}]+)\}$'

        # Search for the pattern in the string
        match = re.search(pattern, s)

        # If a match is found, extract the value and remove the template from the string
        if match:
            value = match.group(1)  # Extracting the value inside the curly braces
            s = re.sub(pattern, '', s)  # Removing the '{value}' part from the string
            return value, s
        else:
            return None, s  # No template found, return None and the original string
