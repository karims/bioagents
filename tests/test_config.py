from pathlib import Path

import pytest
from typer.testing import CliRunner

from bioagents.cli.main import app
from bioagents.core.config import RuntimeConfig
from bioagents.core.registry import get_agent, get_agents, get_blackboard
from bioagents.core.runtime import SwarmRuntime
from bioagents.core.task import load_task


def test_config_model_loads_from_task_json() -> None:
    task = load_task(Path("demos/sample_task.json"))

    assert task.config == RuntimeConfig(
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
        provider=None,
    )

    hypotheses = runtime.run(load_task(Path("demos/document_task.json")))

    assert len(hypotheses) == 1
    assert hypotheses[0].text == "performance issue"


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
