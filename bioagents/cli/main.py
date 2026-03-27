import json
from dataclasses import asdict
from pathlib import Path

import typer

from bioagents.core.agent import Agent, CriticAgent
from bioagents.core.models import Hypothesis, HypothesisSubmission
from bioagents.core.runtime import SwarmRuntime

app = typer.Typer()
run_app = typer.Typer()
app.add_typer(run_app, name="run")


def load_input(input_file: Path) -> dict:
    return json.loads(input_file.read_text())


def build_demo_agents() -> list[Agent]:
    return [
        Agent(
            name="bug_agent",
            outputs=[
                HypothesisSubmission(
                    hypothesis=Hypothesis(
                        text="possible bug",
                        source="bug_agent",
                        confidence=0.6,
                    )
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


@run_app.callback(invoke_without_command=True)
def run(input_file: Path) -> None:
    context = load_input(input_file)
    runtime = SwarmRuntime(agents=build_demo_agents())
    hypotheses = runtime.run(context)
    typer.echo(json.dumps([asdict(hypothesis) for hypothesis in hypotheses], indent=2))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
