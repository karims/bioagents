from dataclasses import dataclass, field

from bioagents.core.models import Hypothesis
from bioagents.core.rules import ReinforceOnRepeatRule, Rule


@dataclass
class Blackboard:
    hypotheses: dict[str, Hypothesis] = field(default_factory=dict)
    rules: list[Rule] = field(default_factory=lambda: [ReinforceOnRepeatRule()])

    def _normalize(self, text: str) -> str:
        return text.strip().lower()

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

    def get_all(self) -> list[Hypothesis]:
        return list(self.hypotheses.values())
