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
