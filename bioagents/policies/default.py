from dataclasses import dataclass

from bioagents.policies.base import Policy


@dataclass
class DefaultPolicy(Policy):
    name: str = "default"
    rules: list[str] | None = None
    similarity_threshold: float | None = 0.85
    reinforcement_bump: float = 0.05
    contradiction_penalty: float = 0.08
    decay_amount: float = 0.02
    prune_threshold: float = 0.3
    trail_increment: float = 0.02
    trail_decay: float = 0.02
    novelty_decay: float = 0.04
    anomaly_decay: float = 0.02

    def __post_init__(self) -> None:
        if self.rules is None:
            self.rules = ["reinforce", "contradict", "decay", "prune"]


@dataclass
class PlaceholderPolicy(Policy):
    name: str = "placeholder"
    rules: list[str] | None = None
    similarity_threshold: float | None = 0.85
    reinforcement_bump: float = 0.05
    contradiction_penalty: float = 0.08
    decay_amount: float = 0.02
    prune_threshold: float = 0.3
    trail_increment: float = 0.02
    trail_decay: float = 0.02
    novelty_decay: float = 0.04
    anomaly_decay: float = 0.02

    def __post_init__(self) -> None:
        if self.rules is None:
            self.rules = ["reinforce", "contradict", "decay", "prune"]
