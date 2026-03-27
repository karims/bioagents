from dataclasses import dataclass, field
from typing import Any

from bioagents.core.agent import Agent
from bioagents.core.blackboard import Blackboard
from bioagents.core.models import Hypothesis


@dataclass
class SwarmRuntime:
    agents: list[Agent]
    max_steps: int = 3
    board: Blackboard = field(default_factory=Blackboard)

    def run(self, context: dict[str, Any]) -> list[Hypothesis]:
        for _ in range(self.max_steps):
            for agent in self.agents:
                outputs = agent.act(context, self.board)
                self.board.add_hypotheses(outputs)
            self.board.apply_step_rules()
        return self.board.get_all()
