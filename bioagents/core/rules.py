from dataclasses import dataclass
from typing import Protocol

from bioagents.core.models import Hypothesis


class Rule(Protocol):
    def apply(self, existing: Hypothesis, incoming: Hypothesis) -> None:
        ...


@dataclass
class ReinforceOnRepeatRule:
    confidence_bump: float = 0.05

    def apply(self, existing: Hypothesis, incoming: Hypothesis) -> None:
        existing.support += 1
        if incoming.source not in existing.sources:
            existing.sources.append(incoming.source)
        existing.confidence = min(1.0, existing.confidence + self.confidence_bump)
