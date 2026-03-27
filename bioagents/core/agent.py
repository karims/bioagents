from dataclasses import dataclass
from typing import Any


@dataclass
class Agent:
    name: str
    outputs: list[str]

    def act(self, context: dict[str, Any], board: Any) -> list[str]:
        return list(self.outputs)
