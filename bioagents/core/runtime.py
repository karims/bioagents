from dataclasses import dataclass, field
from typing import Any

from bioagents.core.agent import Agent
from bioagents.core.blackboard import Blackboard


@dataclass
class SwarmRuntime:
    agents: list[Agent]
    max_steps: int = 3
    board: Blackboard = field(default_factory=Blackboard)

    def run(self, context: dict[str, Any]) -> list[str]:
        for _ in range(self.max_steps):
            for agent in self.agents:
                outputs = agent.act(context, self.board)
                self.board.add(outputs)
        return self.board.get_all()
