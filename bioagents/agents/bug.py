from bioagents.agents.base import Agent
from bioagents.llm.prompts import build_bug_prompt
from bioagents.llm.provider import Provider


class BugAgent(Agent):
    def __init__(self, provider: Provider | None = None):
        super().__init__(
            name="bug_agent",
            skills=["analyze", "evaluate_risk"],
            fallback_text="possible bug",
            provider=provider,
            prompt_builder=build_bug_prompt,
        )
