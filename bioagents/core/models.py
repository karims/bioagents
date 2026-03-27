from dataclasses import dataclass


@dataclass
class Hypothesis:
    text: str
    source: str
    confidence: float = 0.5
