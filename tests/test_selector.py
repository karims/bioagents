from bioagents.policies.ant import AntPolicy
from bioagents.policies.bee import BeePolicy
from bioagents.policies.immune import ImmunePolicy
from bioagents.core.models import Hypothesis
from bioagents.core.selector import HypothesisSelector


def test_selector_sorts_hypotheses_in_expected_order() -> None:
    hypotheses = [
        Hypothesis(text="low", source="a", confidence=0.4, support=5, opposition=0),
        Hypothesis(text="mid", source="b", confidence=0.7, support=2, opposition=1),
        Hypothesis(text="high", source="c", confidence=0.7, support=3, opposition=0),
    ]

    ranked = HypothesisSelector().select(hypotheses)

    assert [hypothesis.text for hypothesis in ranked] == ["high", "mid", "low"]


def test_selector_top_k_truncates_results() -> None:
    hypotheses = [
        Hypothesis(text="a", source="a", confidence=0.9),
        Hypothesis(text="b", source="b", confidence=0.8),
        Hypothesis(text="c", source="c", confidence=0.7),
    ]

    ranked = HypothesisSelector(top_k=2).select(hypotheses)

    assert [hypothesis.text for hypothesis in ranked] == ["a", "b"]


def test_near_duplicates_merge_into_one_cluster() -> None:
    hypotheses = [
        Hypothesis(text="null pointer exception when accessing profile", source="a"),
        Hypothesis(
            text="this may cause a null pointer exception when accessing profile",
            source="b",
        ),
    ]

    ranked = HypothesisSelector(similarity_threshold=0.6).select(hypotheses)

    assert len(ranked) == 1


def test_different_ideas_stay_separate() -> None:
    hypotheses = [
        Hypothesis(text="null pointer exception", source="a"),
        Hypothesis(text="performance issue due to loop", source="b"),
    ]

    ranked = HypothesisSelector(similarity_threshold=0.8).select(hypotheses)

    assert len(ranked) == 2


def test_cluster_aggregation_sums_fields_and_merges_sources() -> None:
    hypotheses = [
        Hypothesis(
            text="null pointer exception when accessing profile",
            source="a",
            confidence=0.7,
            support=2,
            sources=["a"],
            opposition=1,
            critic_sources=["critic_a"],
        ),
        Hypothesis(
            text="this may cause a null pointer exception when accessing profile",
            source="b",
            confidence=0.6,
            support=3,
            sources=["b"],
            opposition=2,
            critic_sources=["critic_b"],
        ),
    ]

    ranked = HypothesisSelector(similarity_threshold=0.6).select(hypotheses)

    assert len(ranked) == 1
    assert ranked[0].support == 5
    assert ranked[0].opposition == 3
    assert ranked[0].confidence == 0.7
    assert ranked[0].sources == ["a", "b"]
    assert ranked[0].critic_sources == ["critic_a", "critic_b"]


def test_clustering_is_more_conservative_for_low_overlap_phrases() -> None:
    hypotheses = [
        Hypothesis(text="shipping risk is high because migration lags", source="a"),
        Hypothesis(text="high confidence fix recommendation for profile guard", source="b"),
    ]

    ranked = HypothesisSelector(similarity_threshold=0.6).select(hypotheses)

    assert len(ranked) == 2


def test_ant_policy_ranks_by_trail_strength() -> None:
    hypotheses = [
        Hypothesis(text="high_conf", source="a", confidence=0.9, trail_strength=0.1),
        Hypothesis(text="strong_trail", source="b", confidence=0.6, trail_strength=0.5),
    ]

    ranked = HypothesisSelector(policy=AntPolicy()).rank(hypotheses)

    assert [hypothesis.text for hypothesis in ranked] == ["strong_trail", "high_conf"]


def test_bee_policy_values_novelty_signal() -> None:
    hypotheses = [
        Hypothesis(text="novel", source="a", confidence=0.5, novelty_score=0.4),
        Hypothesis(text="stable", source="b", confidence=0.52, novelty_score=0.0),
    ]

    ranked = HypothesisSelector(policy=BeePolicy()).rank(hypotheses)

    assert ranked[0].text == "novel"


def test_immune_policy_values_anomaly_signal() -> None:
    hypotheses = [
        Hypothesis(text="fix", source="a", confidence=0.8, anomaly_score=0.0),
        Hypothesis(text="risk", source="b", confidence=0.5, anomaly_score=0.5),
    ]

    ranked = HypothesisSelector(policy=ImmunePolicy()).rank(hypotheses)

    assert ranked[0].text == "risk"
