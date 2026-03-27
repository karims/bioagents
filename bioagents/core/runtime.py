from dataclasses import dataclass, field

from bioagents.core.agent import Agent
from bioagents.core.blackboard import Blackboard
from bioagents.core.config import RuntimeConfig
from bioagents.core.models import Hypothesis
from bioagents.core.registry import get_agents, get_blackboard, resolve_config
from bioagents.core.selector import HypothesisSelector
from bioagents.core.task import Task
from bioagents.llm.provider import Provider


@dataclass
class SwarmRuntime:
    agents: list[Agent]
    max_steps: int = 3
    top_k: int | None = None
    similarity_threshold: float = 0.8
    board: Blackboard = field(default_factory=Blackboard)

    @classmethod
    def from_config(
        cls,
        config: RuntimeConfig | None = None,
        provider: Provider | None = None,
    ) -> "SwarmRuntime":
        resolved = resolve_config(config)
        return cls(
            agents=get_agents(resolved.agents, provider=provider),
            max_steps=resolved.max_steps,
            top_k=resolved.top_k,
            similarity_threshold=resolved.similarity_threshold,
            board=get_blackboard(resolved.rules),
        )

    def run(self, task: Task) -> list[Hypothesis]:
        for _ in range(self.max_steps):
            for agent in self.agents:
                outputs = agent.act(task, self.board)
                self.board.add_submissions(outputs)
            self.board.apply_step_rules()
        return HypothesisSelector(
            top_k=self.top_k,
            similarity_threshold=self.similarity_threshold,
        ).select(self.board.get_all())
