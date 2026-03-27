from bioagents.agents.base import Agent
from bioagents.llm.prompts import build_solution_prompt
from bioagents.llm.provider import Provider


class SolutionAgent(Agent):
    def __init__(self, provider: Provider | None = None):
        super().__init__(
            name="solution_agent",
            skills=["rewrite", "suggest_strategy"],
            fallback_text="add a guard before the risky access",
            provider=provider,
            prompt_builder=build_solution_prompt,
        )
