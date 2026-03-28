from dataclasses import dataclass


@dataclass
class Policy:
    name: str
    rules: list[str] | None = None
    similarity_threshold: float | None = None
    reinforcement_bump: float | None = None
    contradiction_penalty: float | None = None
    decay_amount: float | None = None
    prune_threshold: float | None = None
