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
    trail_increment: float = 0.18
    trail_decay: float = 0.01
    novelty_decay: float = 0.06
    anomaly_decay: float = 0.02

    def __post_init__(self) -> None:
        if self.rules is None:
            self.rules = ["reinforce", "contradict", "decay", "prune"]

    def prepare_hypothesis(self, hypothesis, agent_name: str, step_index: int, max_steps: int) -> None:
        hypothesis.trail_strength = max(hypothesis.trail_strength, 0.12)

    def ranking_key(self, hypothesis) -> tuple[float, float, float, float]:
        return (
            hypothesis.trail_strength,
            hypothesis.confidence,
            float(hypothesis.support),
            -float(hypothesis.opposition),
        )

    def summary_hint(self, hypotheses) -> str | None:
        if not hypotheses:
            return None
        top = max(hypotheses, key=lambda item: item.trail_strength)
        return f"top_trail_strength={top.trail_strength:.2f}"
