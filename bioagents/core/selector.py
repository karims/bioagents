from dataclasses import dataclass

from bioagents.core.models import Hypothesis


@dataclass
class HypothesisSelector:
    top_k: int | None = None

    def select(self, hypotheses: list[Hypothesis]) -> list[Hypothesis]:
        ranked = sorted(
            hypotheses,
            key=lambda hypothesis: (
                hypothesis.confidence,
                hypothesis.support,
                -hypothesis.opposition,
            ),
            reverse=True,
        )
        if self.top_k is None:
            return ranked
        return ranked[: self.top_k]
