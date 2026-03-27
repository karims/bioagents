from dataclasses import dataclass, field

from bioagents.core.models import CritiqueSubmission, Hypothesis, HypothesisSubmission, Submission
from bioagents.core.normalize import normalize_hypothesis_text
from bioagents.core.rules import (
    ContradictRule,
    CritiqueRule,
    DecayRule,
    PruneRule,
    ReinforceOnRepeatRule,
    Rule,
    StepRule,
)


@dataclass
class Blackboard:
    hypotheses: dict[str, Hypothesis] = field(default_factory=dict)
    rules: list[Rule] = field(default_factory=lambda: [ReinforceOnRepeatRule()])
    critique_rules: list[CritiqueRule] = field(default_factory=lambda: [ContradictRule()])
    step_rules: list[StepRule] = field(default_factory=lambda: [DecayRule(), PruneRule()])

    def _normalize(self, text: str) -> str:
        return normalize_hypothesis_text(text)

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        key = self._normalize(hypothesis.text)
        existing = self.hypotheses.get(key)

        if existing is None:
            self.hypotheses[key] = hypothesis
            return

        for rule in self.rules:
            rule.apply(existing, hypothesis)

    def add_hypotheses(self, hypotheses: list[Hypothesis]) -> None:
        for hypothesis in hypotheses:
            self.add_hypothesis(hypothesis)

    def add_critique(self, critique: CritiqueSubmission) -> None:
        key = self._normalize(critique.target_text)
        existing = self.hypotheses.get(key)

        if existing is None:
            return

        for rule in self.critique_rules:
            rule.apply(existing, critique)

    def add_submission(self, submission: Submission) -> None:
        if isinstance(submission, HypothesisSubmission):
            self.add_hypothesis(submission.hypothesis)
            return

        self.add_critique(submission)

    def add_submissions(self, submissions: list[Submission]) -> None:
        for submission in submissions:
            self.add_submission(submission)

    def apply_step_rules(self) -> None:
        for rule in self.step_rules:
            rule.apply(self.hypotheses)

    def get_all(self) -> list[Hypothesis]:
        return list(self.hypotheses.values())
