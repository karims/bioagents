from dataclasses import dataclass
from typing import Any

from bioagents.policies.base import Policy


@dataclass
class ImmunePolicy(Policy):
    name: str = "immune"
    rules: list[str] | None = None
    similarity_threshold: float | None = 0.85
    reinforcement_bump: float = 0.05
    contradiction_penalty: float = 0.12
    decay_amount: float = 0.03
    prune_threshold: float = 0.35
    anomaly_agents: tuple[str, ...] = ("bug_agent", "performance_agent", "critic_agent")
    secondary_agents: tuple[str, ...] = ("strategy_agent",)

    def __post_init__(self) -> None:
        if self.rules is None:
            self.rules = ["reinforce", "contradict", "decay", "prune"]

    def plan_agents(self, agents: list[Any], step_index: int, max_steps: int) -> list[Any]:
        active_names = set(self.anomaly_agents)
        if step_index >= max_steps - 1:
            active_names |= set(self.secondary_agents)
        planned = [agent for agent in agents if agent.name in active_names]
        return planned or list(agents)
