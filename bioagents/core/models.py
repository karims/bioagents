from dataclasses import dataclass, field
from typing import TypeAlias


@dataclass
class Hypothesis:
    text: str
    source: str
    confidence: float = 0.5
    support: int = 1
    sources: list[str] = field(default_factory=list)
    opposition: int = 0
    critic_sources: list[str] = field(default_factory=list)
    trail_strength: float = 0.0
    novelty_score: float = 0.0
    anomaly_score: float = 0.0

    def __post_init__(self) -> None:
        if not self.sources:
            self.sources = [self.source]


@dataclass
class HypothesisSubmission:
    hypothesis: Hypothesis


@dataclass
class CritiqueSubmission:
    target_text: str
    source: str


Submission: TypeAlias = HypothesisSubmission | CritiqueSubmission
