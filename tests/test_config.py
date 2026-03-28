from pathlib import Path

import pytest
from typer.testing import CliRunner

from bioagents.cli.main import app
from bioagents.core.config import RuntimeConfig
from bioagents.core.registry import get_agent, get_agents, get_blackboard, resolve_agents
from bioagents.core.runtime import SwarmRuntime
from bioagents.core.task import load_task
from bioagents.registry.policies import get_policy


def test_config_model_loads_from_task_json() -> None:
    task = load_task(Path("demos/sample_task.json"))

    assert task.config == RuntimeConfig(
        policy=None,
        agents=["bug_agent", "performance_agent", "solution_agent", "strategy_agent", "critic_agent"],
        rules=["reinforce", "contradict", "decay", "prune"],
        max_steps=3,
        top_k=2,
        similarity_threshold=0.8,
    )


def test_agent_registry_resolves_valid_agent_names() -> None:
    agents = get_agents(["bug_agent", "critic_agent"], provider=None)

    assert [agent.name for agent in agents] == ["bug_agent", "critic_agent"]


def test_rule_registry_resolves_valid_rule_names() -> None:
    board = get_blackboard(["reinforce", "contradict", "decay", "prune"])

    assert len(board.rules) == 1
    assert len(board.critique_rules) == 1
    assert len(board.step_rules) == 2


def test_invalid_agent_name_fails_clearly() -> None:
    with pytest.raises(ValueError, match="Unknown agent"):
        get_agent("missing_agent", provider=None)


def test_invalid_rule_name_fails_clearly() -> None:
    with pytest.raises(ValueError, match="Unknown rule"):
        get_blackboard(["missing_rule"])


def test_runtime_respects_config_selected_agents() -> None:
    runtime = SwarmRuntime.from_config(
        RuntimeConfig(agents=["performance_agent"], rules=["reinforce"], max_steps=2),
        task_type="document_analysis",
        provider=None,
    )

    hypotheses = runtime.run(load_task(Path("demos/document_task.json")))

    assert len(hypotheses) == 1
    assert hypotheses[0].text == "performance issue"


def test_task_type_selects_correct_agents() -> None:
    agents = resolve_agents(None, "document_analysis", provider=None)

    assert [agent.name for agent in agents] == [
        "strategy_agent",
        "solution_agent",
        "critic_agent",
    ]


def test_config_agents_override_task_type() -> None:
    agents = resolve_agents(
        RuntimeConfig(agents=["bug_agent"]),
        "document_analysis",
        provider=None,
    )

    assert [agent.name for agent in agents] == ["bug_agent"]


def test_unknown_task_type_falls_back_to_default_agents() -> None:
    agents = resolve_agents(None, "unknown_task_type", provider=None)

    assert [agent.name for agent in agents] == [
        "bug_agent",
        "performance_agent",
        "solution_agent",
        "strategy_agent",
        "critic_agent",
    ]


def test_cli_top_k_overrides_config_top_k() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["run", "demos/sample_task.json", "--top-k", "1"])

    assert result.exit_code == 0
    assert result.stdout.count('"text"') == 1


def test_cli_similarity_threshold_overrides_config() -> None:
    runner = CliRunner()

    result = runner.invoke(
        app,
        ["run", "demos/sample_task.json", "--similarity-threshold", "0.6"],
    )

    assert result.exit_code == 0


def test_default_policy_loads() -> None:
    policy = get_policy("default")

    assert policy.name == "default"
    assert policy.rules == ["reinforce", "contradict", "decay", "prune"]


def test_ant_policy_loads() -> None:
    policy = get_policy("ant")

    assert policy.name == "ant"
    assert policy.reinforcement_bump == 0.08
    assert policy.decay_amount == 0.01


def test_bee_policy_loads() -> None:
    policy = get_policy("bee")

    assert policy.name == "bee"
    assert policy.rules == ["reinforce", "contradict", "decay", "prune"]


def test_config_policy_is_applied() -> None:
    runtime = SwarmRuntime.from_config(
        RuntimeConfig(policy="default"),
        task_type="pr_review",
        provider=None,
    )

    assert runtime.policy_name == "default"


def test_cli_policy_override_works() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["run", "demos/sample_task.json", "--policy", "default", "--top-k", "1"])

    assert result.exit_code == 0
    assert "policy=default" in result.stdout


def test_cli_bee_policy_override_works() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["run", "demos/sample_task.json", "--policy", "bee", "--top-k", "1"])

    assert result.exit_code == 0
    assert "policy=bee" in result.stdout


def test_ant_policy_changes_rule_parameters() -> None:
    default_board = get_blackboard(["reinforce", "decay", "prune"], policy_name="default")
    ant_board = get_blackboard(["reinforce", "decay", "prune"], policy_name="ant")

    assert default_board.rules[0].confidence_bump == 0.05
    assert ant_board.rules[0].confidence_bump == 0.08
    assert default_board.step_rules[0].decay_amount == 0.02
    assert ant_board.step_rules[0].decay_amount == 0.01


def test_ant_policy_preserves_repeated_ideas_more_strongly() -> None:
    default_board = get_blackboard(["reinforce", "decay"], policy_name="default")
    ant_board = get_blackboard(["reinforce", "decay"], policy_name="ant")

    from bioagents.core.models import Hypothesis

    for board in (default_board, ant_board):
        board.add_hypothesis(Hypothesis(text="idea", source="a", confidence=0.6))
        board.add_hypothesis(Hypothesis(text="idea", source="a", confidence=0.6))
        board.apply_step_rules()

    assert ant_board.get_all()[0].confidence > default_board.get_all()[0].confidence


def test_bee_policy_changes_execution_plan() -> None:
    runtime = SwarmRuntime.from_config(
        RuntimeConfig(policy="bee"),
        task_type="pr_review",
        provider=None,
    )

    step_one_agents = runtime.policy.plan_agents(runtime.agents, 0, runtime.max_steps)
    step_three_agents = runtime.policy.plan_agents(runtime.agents, 2, runtime.max_steps)

    assert [agent.name for agent in step_one_agents] == [
        "bug_agent",
        "performance_agent",
        "strategy_agent",
        "critic_agent",
    ]
    assert [agent.name for agent in step_three_agents] == [
        "solution_agent",
        "strategy_agent",
        "critic_agent",
    ]
