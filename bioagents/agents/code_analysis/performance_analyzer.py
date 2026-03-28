from bioagents.agents.base import Agent
from bioagents.llm.prompts import build_performance_prompt
from bioagents.llm.provider import Provider


class PerformanceAnalyzerAgent(Agent):
    def __init__(self, provider: Provider | None = None):
        super().__init__(
            name="performance_agent",
            skills=["analyze", "evaluate_risk"],
            fallback_text="performance issue",
            provider=provider,
            prompt_builder=build_performance_prompt,
        )
