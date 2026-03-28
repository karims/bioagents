from dataclasses import dataclass

from bioagents.policies.base import Policy


@dataclass
class DefaultPolicy(Policy):
    name: str = "default"
    rules: list[str] | None = None
    similarity_threshold: float | None = 0.85

    def __post_init__(self) -> None:
        if self.rules is None:
            self.rules = ["reinforce", "contradict", "decay", "prune"]


@dataclass
class PlaceholderPolicy(Policy):
    name: str = "placeholder"
    rules: list[str] | None = None
    similarity_threshold: float | None = 0.85
