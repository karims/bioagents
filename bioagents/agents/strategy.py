from bioagents.agents.base import Agent
from bioagents.llm.prompts import build_strategy_prompt
from bioagents.llm.provider import Provider


class StrategyAgent(Agent):
    def __init__(self, provider: Provider | None = None):
        super().__init__(
            name="strategy_agent",
            skills=["summarize", "suggest_strategy", "identify_tradeoffs"],
            fallback_text="fix the highest-risk issue first",
            provider=provider,
            prompt_builder=build_strategy_prompt,
        )
