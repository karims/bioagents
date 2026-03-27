from dataclasses import dataclass, field
import sys
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

    def _clean_generated_text(self, text: str) -> str:
        cleaned = next((line.strip() for line in text.splitlines() if line.strip()), "")
        cleaned = cleaned.lstrip("-* ").strip().strip('`"\'')
        return cleaned

    def act(self, task: Task, board: Any) -> list[Submission]:
        if self.outputs:
            return list(self.outputs)

        if self.provider is not None and self.prompt_builder is not None:
            try:
                text = self._clean_generated_text(
                    self.provider.generate(self.prompt_builder(task, board)).strip()
                )
            except Exception:
                provider_name = getattr(self.provider, "mode_name", "provider")
                sys.stderr.write(
                    f"provider_warning={provider_name} generation failed; using fallback\n"
                )
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
