from bioagents.agents.base import Agent
from bioagents.core.blackboard import Blackboard
from bioagents.core.config import RuntimeConfig
from bioagents.core.rules import ContradictRule, DecayRule, PruneRule, ReinforceOnRepeatRule
from bioagents.registry.agents import AGENT_REGISTRY
from bioagents.llm.provider import Provider


DEFAULT_AGENT_NAMES = [
    "bug_agent",
    "performance_agent",
    "solution_agent",
    "strategy_agent",
    "critic_agent",
]
DEFAULT_RULE_NAMES = ["reinforce", "contradict", "decay", "prune"]


def get_agent(name: str, provider: Provider | None = None) -> Agent:
    if name not in AGENT_REGISTRY:
        raise ValueError(f"Unknown agent: {name}")
    return AGENT_REGISTRY[name](provider=provider)


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
