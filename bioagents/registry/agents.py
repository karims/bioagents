from bioagents.agents.code_analysis.bug_detector import BugDetectorAgent
from bioagents.agents.code_analysis.performance_analyzer import PerformanceAnalyzerAgent
from bioagents.agents.evaluation.critic_evaluator import CriticEvaluatorAgent
from bioagents.agents.reasoning.solution_generator import SolutionGeneratorAgent
from bioagents.agents.reasoning.strategy_planner import StrategyPlannerAgent

AGENT_REGISTRY = {
    "bug_agent": BugDetectorAgent,
    "performance_agent": PerformanceAnalyzerAgent,
    "solution_agent": SolutionGeneratorAgent,
    "strategy_agent": StrategyPlannerAgent,
    "critic_agent": CriticEvaluatorAgent,
}
