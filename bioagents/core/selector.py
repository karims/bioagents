from dataclasses import dataclass

from bioagents.core.cluster import cluster_hypotheses, merge_cluster
from bioagents.core.models import Hypothesis
from bioagents.policies.base import Policy
from bioagents.registry.policies import get_policy


@dataclass
class HypothesisSelector:
    top_k: int | None = None
    similarity_threshold: float = 0.85
    policy: Policy | None = None

    def prepare(self, hypotheses: list[Hypothesis]) -> tuple[list[Hypothesis], int]:
        clusters = cluster_hypotheses(hypotheses, threshold=self.similarity_threshold)
        return [merge_cluster(cluster) for cluster in clusters], len(clusters)

    def rank(self, hypotheses: list[Hypothesis]) -> list[Hypothesis]:
        policy = self.policy or get_policy("default")
        ranked = sorted(
            hypotheses,
            key=policy.ranking_key,
            reverse=True,
        )
        if self.top_k is None:
            return ranked
        return ranked[: self.top_k]

    def select(self, hypotheses: list[Hypothesis]) -> list[Hypothesis]:
        hypotheses, _ = self.prepare(hypotheses)
        return self.rank(hypotheses)
