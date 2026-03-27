from dataclasses import dataclass
from difflib import SequenceMatcher

from bioagents.core.models import Hypothesis


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def cluster_hypotheses(
    hypotheses: list[Hypothesis],
    threshold: float = 0.8,
) -> list[list[Hypothesis]]:
    clusters: list[list[Hypothesis]] = []

    for hypothesis in hypotheses:
        placed = False
        for cluster in clusters:
            representative = cluster[0]
            if similarity(hypothesis.text, representative.text) >= threshold:
                cluster.append(hypothesis)
                placed = True
                break

        if not placed:
            clusters.append([hypothesis])

    return clusters


def merge_cluster(cluster: list[Hypothesis]) -> Hypothesis:
    representative = max(cluster, key=lambda hypothesis: (hypothesis.confidence, -len(hypothesis.text)))
    sources = sorted({source for hypothesis in cluster for source in hypothesis.sources})
    critic_sources = sorted(
        {source for hypothesis in cluster for source in hypothesis.critic_sources}
    )

    return Hypothesis(
        text=representative.text,
        source=representative.source,
        confidence=max(hypothesis.confidence for hypothesis in cluster),
        support=sum(hypothesis.support for hypothesis in cluster),
        sources=sources,
        opposition=sum(hypothesis.opposition for hypothesis in cluster),
        critic_sources=critic_sources,
    )
