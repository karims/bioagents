from pathlib import Path

from bioagents.core.config import RuntimeConfig
from bioagents.core.runtime import SwarmRuntime
from bioagents.core.task import Task, load_task


def test_load_task_from_json() -> None:
    task = load_task(Path("demos/sample_task.json"))

    assert task.task_type == "pr_review"
    assert task.title == "Null-safe email access in user scan"
    assert "profile.email" in task.data
    assert task.config == RuntimeConfig(
        agents=["bug_agent", "performance_agent", "critic_agent"],
        rules=["reinforce", "contradict", "decay", "prune"],
        max_steps=3,
        top_k=2,
        similarity_threshold=0.8,
    )


def test_runtime_works_with_task_model() -> None:
    runtime = SwarmRuntime.from_config(provider=None)

    hypotheses = runtime.run(
        Task(
            task_type="document_review",
            title="Release note draft",
            data="The draft claims the rollout is instant, but the migration still runs in batches.",
        )
    )

    assert hypotheses


def test_sample_demo_runs_in_fallback_mode() -> None:
    runtime = SwarmRuntime.from_config(provider=None)

    hypotheses = runtime.run(load_task(Path("demos/sample_task.json")))

    assert hypotheses


def test_document_demo_runs_in_fallback_mode() -> None:
    runtime = SwarmRuntime.from_config(provider=None)

    hypotheses = runtime.run(load_task(Path("demos/document_task.json")))

    assert hypotheses
