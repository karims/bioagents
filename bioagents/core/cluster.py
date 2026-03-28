from dataclasses import dataclass
from difflib import SequenceMatcher

from bioagents.core.models import Hypothesis
from bioagents.core.normalize import normalize_hypothesis_text


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def _token_overlap(a: str, b: str) -> float:
    a_tokens = set(normalize_hypothesis_text(a).split())
    b_tokens = set(normalize_hypothesis_text(b).split())
    if not a_tokens or not b_tokens:
        return 0.0
    return len(a_tokens & b_tokens) / min(len(a_tokens), len(b_tokens))


def cluster_hypotheses(
    hypotheses: list[Hypothesis],
    threshold: float = 0.85,
) -> list[list[Hypothesis]]:
    clusters: list[list[Hypothesis]] = []

    for hypothesis in hypotheses:
        placed = False
        for cluster in clusters:
            representative = cluster[0]
            if (
                similarity(hypothesis.text, representative.text) >= threshold
                and _token_overlap(hypothesis.text, representative.text) >= 0.5
            ):
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
        trail_strength=sum(hypothesis.trail_strength for hypothesis in cluster),
        novelty_score=max(hypothesis.novelty_score for hypothesis in cluster),
        anomaly_score=max(hypothesis.anomaly_score for hypothesis in cluster),
    )
