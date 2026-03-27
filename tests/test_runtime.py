from bioagents.cli.main import build_demo_agents
from bioagents.core.agent import Agent, CriticAgent
from bioagents.core.models import Hypothesis, HypothesisSubmission
from bioagents.core.runtime import SwarmRuntime
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
    runtime = SwarmRuntime(agents=build_demo_agents(provider=None), max_steps=3)

    hypotheses = runtime.run({"task": "pr_review", "data": "loop over users"})

    assert hypotheses
    assert all(isinstance(hypothesis, Hypothesis) for hypothesis in hypotheses)


def test_agents_produce_structured_submissions_without_real_api_calls() -> None:
    agents = build_demo_agents(provider=MockProvider("missing null check"))

    submissions = agents[0].act({"task": "pr_review", "data": "profile.email"}, board=_EmptyBoard())

    assert len(submissions) == 1
    assert isinstance(submissions[0], HypothesisSubmission)
    assert submissions[0].hypothesis.text == "missing null check"


def test_runtime_executes_for_fixed_number_of_steps() -> None:
    runtime = build_runtime()

    hypotheses = runtime.run({"task": "analyze code"})

    assert hypotheses[0].support == 3
    assert hypotheses[1].support == 3


def test_runtime_returns_structured_hypothesis_objects() -> None:
    runtime = build_runtime()

    hypotheses = runtime.run({"task": "analyze code"})

    assert all(isinstance(hypothesis, Hypothesis) for hypothesis in hypotheses)


def test_repeated_agent_outputs_converge_through_blackboard_merging() -> None:
    runtime = build_runtime()

    hypotheses = runtime.run({"task": "analyze code"})

    assert len(hypotheses) == 2


def test_critic_agent_causes_opposition_on_targeted_hypothesis() -> None:
    runtime = build_runtime()

    hypotheses = runtime.run({"task": "analyze code"})
    targeted = next(h for h in hypotheses if h.text == "possible bug")

    assert targeted.opposition == 3
    assert targeted.critic_sources == ["critic_agent"]


class _EmptyBoard:
    def get_all(self) -> list[Hypothesis]:
        return []
