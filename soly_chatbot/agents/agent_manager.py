from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from db_management.models.entities import User
from soly_chatbot.agents.agent import Agent
from dotenv import load_dotenv
from soly_chatbot.agents.config import model

load_dotenv()


class AgentManager:
    _agent = None

    def __init__(self, agent, user_id: str) -> None:
        self.agents = []
        self.conversation = ConversationChain(llm=model,
                                              memory=ConversationBufferMemory(memory_key="history"),
                                              output_parser=StrOutputParser())
        self.user_id = user_id
        self.transition_to(agent)

    def transition_to(self, agent: Agent):
        """
        The Agent Manager allows changing the State object at runtime.
        """
        print(f"Agent Manager: Transition to {type(agent).__name__}")
        self._agent = agent
        self._agent.agent_manager = self
        self.set_conversation_prompt(str(self._agent.prompt))

    async def invoke_input(self, user_input: str) -> None | str:
        """
        This method is called by the user input.
        param: input: str
        """
        return await self._agent.invoke_input(user_input)

    def set_conversation_prompt(self, prompt: str):
        self.conversation.prompt = ChatPromptTemplate.from_messages([
            ("system", prompt),
            "history", "{history}",
            ("user", "{input}")
        ])
        return


