from dataclasses import dataclass, field

from bioagents.core.models import Hypothesis


@dataclass
class Blackboard:
    hypotheses: list[Hypothesis] = field(default_factory=list)

    def add_hypothesis(self, hypothesis: Hypothesis) -> None:
        self.hypotheses.append(hypothesis)

    def add_hypotheses(self, hypotheses: list[Hypothesis]) -> None:
        for hypothesis in hypotheses:
            self.add_hypothesis(hypothesis)

    def get_all(self) -> list[Hypothesis]:
        return list(self.hypotheses)
