import json
from pathlib import Path

import typer

from bioagents.core.agent import Agent
from bioagents.core.runtime import SwarmRuntime

app = typer.Typer()
run_app = typer.Typer()
app.add_typer(run_app, name="run")


def load_input(input_file: Path) -> dict:
    return json.loads(input_file.read_text())


def build_demo_agents() -> list[Agent]:
    return [
        Agent(name="Agent A", outputs=["possible bug"]),
        Agent(name="Agent B", outputs=["performance issue"]),
    ]


@run_app.callback(invoke_without_command=True)
def run(input_file: Path) -> None:
    context = load_input(input_file)
    runtime = SwarmRuntime(agents=build_demo_agents())
    hypotheses = runtime.run(context)
    typer.echo(json.dumps(hypotheses, indent=2))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
