import os
from abc import ABC, abstractmethod
from soly_chatbot.prompts.prompts import GENERAL_PROMPT


class Agent(ABC):

    def __init__(self, agent_manager=None) -> None:
        self._agent_manager = agent_manager
        self.prompt = GENERAL_PROMPT

    @property
    def agent_manager(self):
        return self._agent_manager

    @agent_manager.setter
    def agent_manager(self, agent_manager):
        self._agent_manager = agent_manager

    @abstractmethod
    def invoke_input(self, input: str) -> None:
        pass