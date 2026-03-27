from dataclasses import dataclass
from typing import Any

from bioagents.core.models import Hypothesis


@dataclass
class Agent:
    name: str
    outputs: list[Hypothesis]

    def act(self, context: dict[str, Any], board: Any) -> list[Hypothesis]:
        return list(self.outputs)
