import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bioagents.core.config import RuntimeConfig


@dataclass
class Task:
    task_type: str
    data: str
    title: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    config: RuntimeConfig | None = None


def load_task(input_file: Path) -> Task:
    payload = json.loads(input_file.read_text())
    config_payload = payload.get("config")
    config = None
    if config_payload is not None:
        config = RuntimeConfig(
            agents=config_payload.get("agents"),
            rules=config_payload.get("rules"),
            max_steps=config_payload.get("max_steps", 3),
            top_k=config_payload.get("top_k"),
        )
    return Task(
        task_type=payload.get("task_type", payload.get("task", "task")),
        title=payload.get("title"),
        data=payload["data"],
        metadata=payload.get("metadata", {}),
        config=config,
    )
