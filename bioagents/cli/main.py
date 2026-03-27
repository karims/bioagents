import json
from dataclasses import asdict
from pathlib import Path

import typer

from bioagents.core.agent import Agent, CriticAgent
from bioagents.core.runtime import SwarmRuntime
from bioagents.core.task import Task, load_task
from bioagents.llm.prompts import build_bug_prompt, build_performance_prompt
from bioagents.llm.provider import Provider, get_provider_from_env

app = typer.Typer()
run_app = typer.Typer()
app.add_typer(run_app, name="run")


def build_demo_agents(provider: Provider | None = None) -> list[Agent]:
    return [
        Agent(
            name="bug_agent",
            fallback_text="possible bug",
            provider=provider,
            prompt_builder=build_bug_prompt,
        ),
        Agent(
            name="performance_agent",
            fallback_text="performance issue",
            provider=provider,
            prompt_builder=build_performance_prompt,
        ),
        CriticAgent(name="critic_agent"),
    ]


@run_app.callback(invoke_without_command=True)
def run(input_file: Path) -> None:
    task = load_task(input_file)
    mode, provider = get_provider_from_env()
    typer.echo(f"mode={mode}", err=True)
    runtime = SwarmRuntime(agents=build_demo_agents(provider=provider))
    hypotheses = runtime.run(task)
    typer.echo(json.dumps([asdict(hypothesis) for hypothesis in hypotheses], indent=2))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
