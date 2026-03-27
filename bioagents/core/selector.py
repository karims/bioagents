from dataclasses import dataclass

from bioagents.core.cluster import cluster_hypotheses, merge_cluster
from bioagents.core.models import Hypothesis


@dataclass
class HypothesisSelector:
    top_k: int | None = None
    similarity_threshold: float = 0.85

    def prepare(self, hypotheses: list[Hypothesis]) -> tuple[list[Hypothesis], int]:
        clusters = cluster_hypotheses(hypotheses, threshold=self.similarity_threshold)
        return [merge_cluster(cluster) for cluster in clusters], len(clusters)

    def rank(self, hypotheses: list[Hypothesis]) -> list[Hypothesis]:
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

    def select(self, hypotheses: list[Hypothesis]) -> list[Hypothesis]:
        hypotheses, _ = self.prepare(hypotheses)
        return self.rank(hypotheses)
