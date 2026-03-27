from bioagents.agents.base import CriticAgent
from bioagents.llm.provider import Provider


class BuiltinCriticAgent(CriticAgent):
    def __init__(self, provider: Provider | None = None):
        super().__init__(name="critic_agent")
