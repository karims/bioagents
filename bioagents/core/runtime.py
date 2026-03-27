from dataclasses import dataclass, field

from bioagents.core.agent import Agent
from bioagents.core.blackboard import Blackboard
from bioagents.core.models import Hypothesis
from bioagents.core.selector import HypothesisSelector
from bioagents.core.task import Task


@dataclass
class SwarmRuntime:
    agents: list[Agent]
    max_steps: int = 3
    top_k: int | None = None
    board: Blackboard = field(default_factory=Blackboard)

    def run(self, task: Task) -> list[Hypothesis]:
        for _ in range(self.max_steps):
            for agent in self.agents:
                outputs = agent.act(task, self.board)
                self.board.add_submissions(outputs)
            self.board.apply_step_rules()
        return HypothesisSelector(top_k=self.top_k).select(self.board.get_all())
