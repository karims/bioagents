from dataclasses import dataclass, field
from time import perf_counter
from typing import Callable

from bioagents.core.agent import Agent
from bioagents.core.blackboard import Blackboard
from bioagents.core.config import RuntimeConfig
from bioagents.core.models import Hypothesis, HypothesisSubmission
from bioagents.core.registry import get_blackboard, resolve_agents, resolve_config
from bioagents.core.selector import HypothesisSelector
from bioagents.core.task import Task
from bioagents.llm.provider import Provider
from bioagents.policies.base import Policy
from bioagents.registry.policies import get_policy


@dataclass
class SwarmRuntime:
    agents: list[Agent]
    max_steps: int = 3
    top_k: int | None = None
    similarity_threshold: float = 0.85
    policy_name: str = "default"
    policy: Policy = field(default_factory=lambda: get_policy("default"))
    board: Blackboard = field(default_factory=Blackboard)

    @classmethod
    def from_config(
        cls,
        config: RuntimeConfig | None = None,
        task_type: str | None = None,
        provider: Provider | None = None,
    ) -> "SwarmRuntime":
        resolved = resolve_config(config)
        policy = get_policy(resolved.policy)
        return cls(
            agents=resolve_agents(resolved, task_type, provider=provider),
            max_steps=resolved.max_steps,
            top_k=resolved.top_k,
            similarity_threshold=resolved.similarity_threshold,
            policy_name=policy.name,
            policy=policy,
            board=get_blackboard(resolved.rules, policy_name=resolved.policy),
        )

    def run(self, task: Task) -> list[Hypothesis]:
        return self._run(task)[0]

    def run_with_telemetry(
        self,
        task: Task,
        mode: str,
        emit: Callable[[str], None],
    ) -> list[Hypothesis]:
        emit(f"mode={mode}")
        emit(f"policy={self.policy_name}")
        emit(f"task_type={task.task_type}")
        if task.objective:
            emit(f"objective={task.objective}")
        emit(f"agents={','.join(agent.name for agent in self.agents)}")
        emit(f"steps={self.max_steps}")
        hypotheses, total_runtime, hypotheses_generated, clusters_formed, effective_mode = self._run(
            task,
            emit=emit,
            initial_mode=mode,
        )
        if effective_mode != mode:
            emit(f"mode={effective_mode}")
        emit("summary:")
        emit(f"hypotheses_generated={hypotheses_generated}")
        emit(f"clusters_formed={clusters_formed}")
        emit(f"final_returned={len(hypotheses)}")
        emit(f"top_k={self.top_k if self.top_k is not None else 'none'}")
        emit(f"total_runtime={total_runtime:.2f}s")
        return hypotheses

    def _run(
        self,
        task: Task,
        emit: Callable[[str], None] | None = None,
        initial_mode: str = "fallback",
    ) -> tuple[list[Hypothesis], float, int, int, str]:
        total_start = perf_counter()
        hypotheses_generated = 0
        effective_mode = initial_mode

        for _ in range(self.max_steps):
            step_start = perf_counter()
            step_agents = self.policy.plan_agents(self.agents, _, self.max_steps)
            if emit is not None:
                emit(f"step={_ + 1}")
            for agent in step_agents:
                agent_start = perf_counter()
                outputs = agent.act(task, self.board)
                agent_runtime = perf_counter() - agent_start
                self.board.add_submissions(outputs)
                hypotheses_generated += sum(1 for output in outputs if isinstance(output, HypothesisSubmission))
                if emit is not None:
                    agent_mode = "llm" if getattr(agent, "provider", None) is not None else "local"
                    emit(f"{agent.name} mode={agent_mode} time={agent_runtime:.2f}s")
                    warning = getattr(agent, "last_provider_warning", None)
                    if warning is not None:
                        emit(warning)
                        if initial_mode != "fallback":
                            effective_mode = "mixed"
            self.board.apply_step_rules()
            if emit is not None:
                emit(f"step_time={perf_counter() - step_start:.2f}s")

        selector = HypothesisSelector(
            top_k=self.top_k,
            similarity_threshold=self.similarity_threshold,
        )
        merged_hypotheses, clusters_formed = selector.prepare(self.board.get_all())
        ranked = selector.rank(merged_hypotheses)
        return ranked, perf_counter() - total_start, hypotheses_generated, clusters_formed, effective_mode
