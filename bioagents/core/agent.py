from dataclasses import dataclass, field
from typing import Any, Callable

from bioagents.core.models import CritiqueSubmission, Hypothesis, HypothesisSubmission, Submission
from bioagents.core.skills import get_skill_descriptions
from bioagents.core.task import Task
from bioagents.llm.provider import Provider


@dataclass
class Agent:
    name: str
    skills: list[str] = field(default_factory=list)
    outputs: list[Submission] = field(default_factory=list)
    fallback_text: str | None = None
    provider: Provider | None = None
    prompt_builder: Callable[[Task, Any, list[str], list[str]], str] | None = None
    last_provider_warning: str | None = field(default=None, init=False)

    def _clean_generated_text(self, text: str) -> str:
        cleaned = next((line.strip() for line in text.splitlines() if line.strip()), "")
        cleaned = cleaned.lstrip("-* ").strip().strip('`"\'')
        return cleaned

    def act(self, task: Task, board: Any) -> list[Submission]:
        self.last_provider_warning = None

        if self.outputs:
            return list(self.outputs)

        if self.provider is not None and self.prompt_builder is not None:
            try:
                text = self._clean_generated_text(
                    self.provider.generate(
                        self.prompt_builder(task, board, self.skills, get_skill_descriptions(self.skills))
                    ).strip()
                )
            except Exception:
                provider_name = getattr(self.provider, "mode_name", "provider")
                self.last_provider_warning = (
                    f"provider_warning={provider_name} generation failed; using fallback"
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
    skills: list[str] = field(default_factory=lambda: ["evaluate_risk", "identify_tradeoffs"])
    last_provider_warning: str | None = field(default=None, init=False)

    def act(self, task: Task, board: Any) -> list[Submission]:
        self.last_provider_warning = None
        hypotheses = board.get_all()
        if not hypotheses:
            return []

        target = hypotheses[0]
        return [CritiqueSubmission(target_text=target.text, source=self.name)]
