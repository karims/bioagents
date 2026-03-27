from dataclasses import dataclass, field


@dataclass
class Blackboard:
    hypotheses: list[str] = field(default_factory=list)

    def add_hypothesis(self, hypothesis: str) -> None:
        self.hypotheses.append(hypothesis)

    def add(self, hypotheses: list[str]) -> None:
        for hypothesis in hypotheses:
            self.add_hypothesis(hypothesis)

    def get_all(self) -> list[str]:
        return list(self.hypotheses)
