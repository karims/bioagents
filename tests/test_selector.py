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
