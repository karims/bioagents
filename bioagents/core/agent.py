from dataclasses import dataclass
from typing import Any

from bioagents.core.models import CritiqueSubmission, Submission


@dataclass
class Agent:
    name: str
    outputs: list[Submission]

    def act(self, context: dict[str, Any], board: Any) -> list[Submission]:
        return list(self.outputs)


@dataclass
class CriticAgent:
    name: str

    def act(self, context: dict[str, Any], board: Any) -> list[Submission]:
        hypotheses = board.get_all()
        if not hypotheses:
            return []

        target = hypotheses[0]
        return [CritiqueSubmission(target_text=target.text, source=self.name)]
