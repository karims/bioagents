from dataclasses import dataclass

from bioagents.core.cluster import cluster_hypotheses, merge_cluster
from bioagents.core.models import Hypothesis


@dataclass
class HypothesisSelector:
    top_k: int | None = None
    similarity_threshold: float = 0.8

    def select(self, hypotheses: list[Hypothesis]) -> list[Hypothesis]:
        clusters = cluster_hypotheses(hypotheses, threshold=self.similarity_threshold)
        hypotheses = [merge_cluster(cluster) for cluster in clusters]
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
