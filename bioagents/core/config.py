from dataclasses import dataclass


@dataclass
class RuntimeConfig:
    agents: list[str] | None = None
    rules: list[str] | None = None
    max_steps: int = 3
    top_k: int | None = None
    similarity_threshold: float = 0.8
