from dataclasses import dataclass


@dataclass
class Policy:
    name: str
    rules: list[str] | None = None
    similarity_threshold: float | None = None
