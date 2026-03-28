from dataclasses import dataclass

from bioagents.core.models import Hypothesis


@dataclass
class Policy:
    name: str
    rules: list[str] | None = None
    similarity_threshold: float | None = None
    reinforcement_bump: float | None = None
    contradiction_penalty: float | None = None
    decay_amount: float | None = None
    prune_threshold: float | None = None
    trail_increment: float | None = None
    trail_decay: float | None = None
    novelty_decay: float | None = None
    anomaly_decay: float | None = None

    def plan_agents(self, agents: list[object], step_index: int, max_steps: int) -> list[object]:
        return list(agents)

    def prepare_hypothesis(
        self,
        hypothesis: Hypothesis,
        agent_name: str,
        step_index: int,
        max_steps: int,
    ) -> None:
        return None

    def ranking_key(self, hypothesis: Hypothesis) -> tuple[float, float, float, float]:
        return (
            hypothesis.confidence,
            float(hypothesis.support),
            -float(hypothesis.opposition),
            0.0,
        )

    def summary_hint(self, hypotheses: list[Hypothesis]) -> str | None:
        return None
