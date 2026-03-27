from dataclasses import dataclass
from typing import Protocol

from bioagents.core.models import CritiqueSubmission, Hypothesis


class Rule(Protocol):
    def apply(self, existing: Hypothesis, incoming: Hypothesis) -> None:
        ...


class CritiqueRule(Protocol):
    def apply(self, existing: Hypothesis, critique: CritiqueSubmission) -> None:
        ...


class StepRule(Protocol):
    def apply(self, hypotheses: dict[str, Hypothesis]) -> None:
        ...


@dataclass
class ReinforceOnRepeatRule:
    confidence_bump: float = 0.05

    def apply(self, existing: Hypothesis, incoming: Hypothesis) -> None:
        existing.support += 1
        if incoming.source not in existing.sources:
            existing.sources.append(incoming.source)
        existing.confidence = min(1.0, existing.confidence + self.confidence_bump)


@dataclass
class ContradictRule:
    confidence_penalty: float = 0.08

    def apply(self, existing: Hypothesis, critique: CritiqueSubmission) -> None:
        existing.opposition += 1
        if critique.source not in existing.critic_sources:
            existing.critic_sources.append(critique.source)
        existing.confidence = max(0.0, existing.confidence - self.confidence_penalty)


@dataclass
class DecayRule:
    decay_amount: float = 0.02

    def apply(self, hypotheses: dict[str, Hypothesis]) -> None:
        for hypothesis in hypotheses.values():
            hypothesis.confidence = max(0.0, hypothesis.confidence - self.decay_amount)


@dataclass
class PruneRule:
    threshold: float = 0.3

    def apply(self, hypotheses: dict[str, Hypothesis]) -> None:
        to_remove = [
            key for key, hypothesis in hypotheses.items() if hypothesis.confidence < self.threshold
        ]
        for key in to_remove:
            del hypotheses[key]
