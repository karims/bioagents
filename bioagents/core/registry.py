from bioagents.core.agent import Agent, CriticAgent
from bioagents.core.blackboard import Blackboard
from bioagents.core.config import RuntimeConfig
from bioagents.core.rules import ContradictRule, DecayRule, PruneRule, ReinforceOnRepeatRule
from bioagents.llm.prompts import build_bug_prompt, build_performance_prompt
from bioagents.llm.provider import Provider


DEFAULT_AGENT_NAMES = ["bug_agent", "performance_agent", "critic_agent"]
DEFAULT_RULE_NAMES = ["reinforce", "contradict", "decay", "prune"]


def get_agent(name: str, provider: Provider | None = None) -> Agent:
    if name == "bug_agent":
        return Agent(
            name="bug_agent",
            fallback_text="possible bug",
            provider=provider,
            prompt_builder=build_bug_prompt,
        )
    if name == "performance_agent":
        return Agent(
            name="performance_agent",
            fallback_text="performance issue",
            provider=provider,
            prompt_builder=build_performance_prompt,
        )
    if name == "critic_agent":
        return CriticAgent(name="critic_agent")
    raise ValueError(f"Unknown agent: {name}")


def get_agents(names: list[str] | None, provider: Provider | None = None) -> list[Agent]:
    selected_names = names or DEFAULT_AGENT_NAMES
    return [get_agent(name, provider=provider) for name in selected_names]


def get_blackboard(names: list[str] | None) -> Blackboard:
    selected_names = names or DEFAULT_RULE_NAMES
    rules = []
    critique_rules = []
    step_rules = []

    for name in selected_names:
        if name == "reinforce":
            rules.append(ReinforceOnRepeatRule())
            continue
        if name == "contradict":
            critique_rules.append(ContradictRule())
            continue
        if name == "decay":
            step_rules.append(DecayRule())
            continue
        if name == "prune":
            step_rules.append(PruneRule())
            continue
        raise ValueError(f"Unknown rule: {name}")

    return Blackboard(rules=rules, critique_rules=critique_rules, step_rules=step_rules)


def resolve_config(config: RuntimeConfig | None) -> RuntimeConfig:
    return config or RuntimeConfig()
