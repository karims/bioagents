from pathlib import Path

import pytest

from bioagents.core.registry import get_agent
from bioagents.core.skills import SKILLS, get_skill_description
from bioagents.core.task import Task, load_task
from bioagents.llm.prompts import build_bug_prompt


def test_task_objective_loads_correctly() -> None:
    task = load_task(Path("demos/sample_task.json"))

    assert task.objective == "identify the main risks and suggest the most useful improvement"


def test_skills_registry_resolves_known_skills() -> None:
    assert "analyze" in SKILLS
    assert get_skill_description("suggest_strategy")


def test_skills_registry_rejects_unknown_skills() -> None:
    with pytest.raises(ValueError, match="Unknown skill"):
        get_skill_description("missing_skill")


def test_agents_expose_expected_skills() -> None:
    bug_agent = get_agent("bug_agent", provider=None)
    strategy_agent = get_agent("strategy_agent", provider=None)

    assert bug_agent.skills == ["analyze", "evaluate_risk"]
    assert strategy_agent.skills == ["summarize", "suggest_strategy", "identify_tradeoffs"]


def test_prompts_include_objective_and_skills() -> None:
    bug_agent = get_agent("bug_agent", provider=None)
    prompt = build_bug_prompt(
        Task(
            task_type="pr_review",
            data="profile.email access",
            objective="identify the main risks and suggest the most useful improvement",
        ),
        _EmptyBoard(),
        bug_agent.skills,
        [get_skill_description(skill) for skill in bug_agent.skills],
    )

    assert "Objective: identify the main risks and suggest the most useful improvement" in prompt
    assert "Skills:" in prompt


class _EmptyBoard:
    def get_all(self) -> list[object]:
        return []
