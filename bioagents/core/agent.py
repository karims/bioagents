from dataclasses import dataclass, field
from typing import Any, Callable

from bioagents.core.models import CritiqueSubmission, Hypothesis, HypothesisSubmission, Submission
from bioagents.core.task import Task
from bioagents.llm.provider import Provider


@dataclass
class Agent:
    name: str
    outputs: list[Submission] = field(default_factory=list)
    fallback_text: str | None = None
    provider: Provider | None = None
    prompt_builder: Callable[[Task, Any], str] | None = None

    def act(self, task: Task, board: Any) -> list[Submission]:
        if self.outputs:
            return list(self.outputs)

        if self.provider is not None and self.prompt_builder is not None:
            try:
                text = self.provider.generate(self.prompt_builder(task, board)).strip()
            except Exception:
                text = ""
            if text:
                return [HypothesisSubmission(hypothesis=Hypothesis(text=text, source=self.name))]

        if self.fallback_text:
            return [
                HypothesisSubmission(
                    hypothesis=Hypothesis(text=self.fallback_text, source=self.name)
                )
            ]

        return []


@dataclass
class CriticAgent:
    name: str

    def act(self, task: Task, board: Any) -> list[Submission]:
        hypotheses = board.get_all()
        if not hypotheses:
            return []

        target = hypotheses[0]
        return [CritiqueSubmission(target_text=target.text, source=self.name)]
