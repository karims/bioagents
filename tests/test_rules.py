from bioagents.core.models import CritiqueSubmission, Hypothesis
from bioagents.core.rules import ContradictRule, DecayRule, PruneRule, ReinforceOnRepeatRule


def test_reinforcement_rule_increases_confidence_but_not_above_one() -> None:
    rule = ReinforceOnRepeatRule()
    existing = Hypothesis(text="idea", source="agent_a", confidence=0.98)
    incoming = Hypothesis(text="idea", source="agent_b", confidence=0.6)

    rule.apply(existing, incoming)

    assert existing.confidence == 1.0


def test_decay_rule_lowers_confidence() -> None:
    rule = DecayRule()
    hypotheses = {"idea": Hypothesis(text="idea", source="agent_a", confidence=0.6)}

    rule.apply(hypotheses)

    assert hypotheses["idea"].confidence == 0.58


def test_decay_rule_does_not_go_below_zero() -> None:
    rule = DecayRule()
    hypotheses = {"idea": Hypothesis(text="idea", source="agent_a", confidence=0.01)}

    rule.apply(hypotheses)

    assert hypotheses["idea"].confidence == 0.0


def test_prune_rule_removes_low_confidence_hypotheses() -> None:
    rule = PruneRule()
    hypotheses = {"idea": Hypothesis(text="idea", source="agent_a", confidence=0.29)}

    rule.apply(hypotheses)

    assert hypotheses == {}


def test_prune_rule_keeps_sufficiently_strong_hypotheses() -> None:
    rule = PruneRule()
    hypotheses = {"idea": Hypothesis(text="idea", source="agent_a", confidence=0.3)}

    rule.apply(hypotheses)

    assert "idea" in hypotheses


def test_contradict_rule_increases_opposition_and_reduces_confidence() -> None:
    rule = ContradictRule()
    hypothesis = Hypothesis(text="idea", source="agent_a", confidence=0.6)

    rule.apply(hypothesis, CritiqueSubmission(target_text="idea", source="critic"))

    assert hypothesis.opposition == 1
    assert hypothesis.critic_sources == ["critic"]
    assert hypothesis.confidence == 0.52
