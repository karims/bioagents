from bioagents.core.blackboard import Blackboard
from bioagents.core.models import CritiqueSubmission, Hypothesis, HypothesisSubmission


def test_repeated_hypotheses_with_normalized_text_are_merged() -> None:
    board = Blackboard(step_rules=[])

    board.add_submission(
        HypothesisSubmission(Hypothesis(text="Possible Bug", source="agent_a", confidence=0.6))
    )
    board.add_submission(
        HypothesisSubmission(Hypothesis(text=" possible bug ", source="agent_b", confidence=0.7))
    )

    hypotheses = board.get_all()

    assert len(hypotheses) == 1
    assert hypotheses[0].text == "Possible Bug"


def test_support_count_increases_on_repeated_submissions() -> None:
    board = Blackboard(step_rules=[])

    board.add_submission(HypothesisSubmission(Hypothesis(text="idea", source="agent_a")))
    board.add_submission(HypothesisSubmission(Hypothesis(text="idea", source="agent_a")))

    hypothesis = board.get_all()[0]

    assert hypothesis.support == 2


def test_sources_are_accumulated_uniquely() -> None:
    board = Blackboard(step_rules=[])

    board.add_submission(HypothesisSubmission(Hypothesis(text="idea", source="agent_a")))
    board.add_submission(HypothesisSubmission(Hypothesis(text="idea", source="agent_b")))
    board.add_submission(HypothesisSubmission(Hypothesis(text="idea", source="agent_b")))

    hypothesis = board.get_all()[0]

    assert hypothesis.sources == ["agent_a", "agent_b"]


def test_critique_submissions_increase_opposition() -> None:
    board = Blackboard(step_rules=[])

    board.add_submission(HypothesisSubmission(Hypothesis(text="idea", source="agent_a")))
    board.add_submission(CritiqueSubmission(target_text="idea", source="critic"))

    hypothesis = board.get_all()[0]

    assert hypothesis.opposition == 1
    assert hypothesis.critic_sources == ["critic"]


def test_critique_submissions_reduce_confidence() -> None:
    board = Blackboard(step_rules=[])

    board.add_submission(HypothesisSubmission(Hypothesis(text="idea", source="agent_a", confidence=0.6)))
    board.add_submission(CritiqueSubmission(target_text="idea", source="critic"))

    hypothesis = board.get_all()[0]

    assert hypothesis.confidence == 0.52


def test_critique_targeting_missing_hypothesis_is_ignored() -> None:
    board = Blackboard(step_rules=[])

    board.add_submission(CritiqueSubmission(target_text="missing", source="critic"))

    assert board.get_all() == []
