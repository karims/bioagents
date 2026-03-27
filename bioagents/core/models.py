from dataclasses import dataclass, field


@dataclass
class Hypothesis:
    text: str
    source: str
    confidence: float = 0.5
    support: int = 1
    sources: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.sources:
            self.sources = [self.source]
