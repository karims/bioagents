from dataclasses import dataclass

from bioagents.policies.base import Policy


@dataclass
class AntPolicy(Policy):
    name: str = "ant"
    rules: list[str] | None = None
    similarity_threshold: float | None = 0.85
    reinforcement_bump: float = 0.08
    contradiction_penalty: float = 0.08
    decay_amount: float = 0.01
    prune_threshold: float = 0.25

    def __post_init__(self) -> None:
        if self.rules is None:
            self.rules = ["reinforce", "contradict", "decay", "prune"]
