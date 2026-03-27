from bioagents.agents.bug import BugAgent
from bioagents.agents.critic import BuiltinCriticAgent
from bioagents.agents.performance import PerformanceAgent
from bioagents.agents.solution import SolutionAgent
from bioagents.agents.strategy import StrategyAgent

AGENT_REGISTRY = {
    "bug_agent": BugAgent,
    "performance_agent": PerformanceAgent,
    "solution_agent": SolutionAgent,
    "strategy_agent": StrategyAgent,
    "critic_agent": BuiltinCriticAgent,
}
