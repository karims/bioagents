from bioagents.core.agent import Agent, CriticAgent
from bioagents.core.models import Hypothesis, HypothesisSubmission
from bioagents.core.runtime import SwarmRuntime


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
