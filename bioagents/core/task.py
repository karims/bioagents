import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Task:
    task_type: str
    data: str
    title: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


def load_task(input_file: Path) -> Task:
    payload = json.loads(input_file.read_text())
    return Task(
        task_type=payload.get("task_type", payload.get("task", "task")),
        title=payload.get("title"),
        data=payload["data"],
        metadata=payload.get("metadata", {}),
    )
