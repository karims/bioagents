from dataclasses import dataclass
from math import ceil
from typing import Any

from bioagents.policies.base import Policy


@dataclass
class BeePolicy(Policy):
    name: str = "bee"
    rules: list[str] | None = None
    similarity_threshold: float | None = 0.85
    reinforcement_bump: float = 0.05
    contradiction_penalty: float = 0.08
    decay_amount: float = 0.02
    prune_threshold: float = 0.3
    scout_agents: tuple[str, ...] = ("bug_agent", "performance_agent", "strategy_agent")
    worker_agents: tuple[str, ...] = ("solution_agent",)
    critic_agents: tuple[str, ...] = ("critic_agent",)

    def __post_init__(self) -> None:
        if self.rules is None:
            self.rules = ["reinforce", "contradict", "decay", "prune"]

    def plan_agents(self, agents: list[Any], step_index: int, max_steps: int) -> list[Any]:
        exploration_steps = max(1, ceil(max_steps / 2))
        if step_index < exploration_steps:
            active_names = set(self.scout_agents) | set(self.critic_agents)
        else:
            active_names = set(self.worker_agents) | set(self.critic_agents) | {"strategy_agent"}
        planned = [agent for agent in agents if agent.name in active_names]
        return planned or list(agents)
