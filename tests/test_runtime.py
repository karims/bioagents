from bioagents.core.agent import Agent, CriticAgent
from bioagents.core.config import RuntimeConfig
from bioagents.core.models import Hypothesis, HypothesisSubmission
from bioagents.core.registry import get_agents
from bioagents.core.runtime import SwarmRuntime
from bioagents.core.task import Task
from bioagents.llm.provider import MockProvider


def build_runtime() -> SwarmRuntime:
    agents = [
        Agent(
            name="bug_agent",
            outputs=[
                HypothesisSubmission(
                    hypothesis=Hypothesis(text="possible bug", source="bug_agent", confidence=0.6)
                )
            ],
        ),
        Agent(
            name="performance_agent",
            outputs=[
                HypothesisSubmission(
                    hypothesis=Hypothesis(
                        text="performance issue",
                        source="performance_agent",
                        confidence=0.55,
                    )
                )
            ],
        ),
        CriticAgent(name="critic_agent"),
    ]
    return SwarmRuntime(agents=agents, max_steps=3)


def test_runtime_runs_without_env_vars() -> None:
    runtime = SwarmRuntime.from_config(provider=None)

    hypotheses = runtime.run(Task(task_type="pr_review", data="loop over users"))

    assert hypotheses
    assert all(isinstance(hypothesis, Hypothesis) for hypothesis in hypotheses)


def test_agents_produce_structured_submissions_without_real_api_calls() -> None:
    agents = get_agents(None, provider=MockProvider("missing null check"))

    submissions = agents[0].act(Task(task_type="pr_review", data="profile.email"), board=_EmptyBoard())

    assert len(submissions) == 1
    assert isinstance(submissions[0], HypothesisSubmission)
    assert submissions[0].hypothesis.text == "missing null check"


def test_runtime_executes_for_fixed_number_of_steps() -> None:
    runtime = build_runtime()

    hypotheses = runtime.run(Task(task_type="analyze_code", data="dummy input"))

    assert hypotheses[0].support == 3
    assert hypotheses[1].support == 3


def test_runtime_returns_structured_hypothesis_objects() -> None:
    runtime = build_runtime()

    hypotheses = runtime.run(Task(task_type="analyze_code", data="dummy input"))

    assert all(isinstance(hypothesis, Hypothesis) for hypothesis in hypotheses)


def test_repeated_agent_outputs_converge_through_blackboard_merging() -> None:
    runtime = build_runtime()

    hypotheses = runtime.run(Task(task_type="analyze_code", data="dummy input"))

    assert len(hypotheses) == 2


def test_critic_agent_causes_opposition_on_targeted_hypothesis() -> None:
    runtime = build_runtime()

    hypotheses = runtime.run(Task(task_type="analyze_code", data="dummy input"))
    targeted = next(h for h in hypotheses if h.text == "possible bug")

    assert targeted.opposition == 3
    assert targeted.critic_sources == ["critic_agent"]


def test_runtime_returns_ranked_output() -> None:
    runtime = build_runtime()

    hypotheses = runtime.run(Task(task_type="analyze_code", data="dummy input"))

    assert [hypothesis.text for hypothesis in hypotheses] == [
        "performance issue",
        "possible bug",
    ]


def test_runtime_top_k_limits_final_results() -> None:
    runtime = SwarmRuntime(agents=build_runtime().agents, max_steps=3, top_k=1)

    hypotheses = runtime.run(Task(task_type="analyze_code", data="dummy input"))

    assert len(hypotheses) == 1


def test_runtime_respects_config_selected_agents_and_rules() -> None:
    runtime = SwarmRuntime.from_config(
        RuntimeConfig(
            agents=["bug_agent", "performance_agent"],
            rules=["reinforce"],
            max_steps=2,
            top_k=1,
        ),
        provider=None,
    )

    hypotheses = runtime.run(Task(task_type="analyze_code", data="dummy input"))

    assert len(hypotheses) == 1
    assert hypotheses[0].opposition == 0
    assert hypotheses[0].support == 2


class _EmptyBoard:
    def get_all(self) -> list[Hypothesis]:
        return []
