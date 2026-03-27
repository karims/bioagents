import json
from dataclasses import asdict
from pathlib import Path

import typer

from bioagents.core.config import RuntimeConfig
from bioagents.core.runtime import SwarmRuntime
from bioagents.core.task import load_task
from bioagents.llm.provider import get_provider_from_env

app = typer.Typer()


@app.command("run")
def run(
    input_file: Path,
    top_k: int | None = typer.Option(default=None, help="Return only the top ranked results."),
    similarity_threshold: float | None = typer.Option(
        default=None,
        help="Merge near-duplicate final hypotheses at or above this similarity threshold.",
    ),
) -> None:
    task = load_task(input_file)
    mode, provider = get_provider_from_env()
    typer.echo(f"mode={mode}", err=True)
    config = task.config or RuntimeConfig()
    if top_k is not None:
        config = RuntimeConfig(
            agents=config.agents,
            rules=config.rules,
            max_steps=config.max_steps,
            top_k=top_k,
            similarity_threshold=config.similarity_threshold,
        )
    if similarity_threshold is not None:
        config = RuntimeConfig(
            agents=config.agents,
            rules=config.rules,
            max_steps=config.max_steps,
            top_k=config.top_k,
            similarity_threshold=similarity_threshold,
        )
    runtime = SwarmRuntime.from_config(config=config, provider=provider)
    hypotheses = runtime.run(task)
    typer.echo(json.dumps([asdict(hypothesis) for hypothesis in hypotheses], indent=2))


@app.command(hidden=True)
def _unused() -> None:
    pass


def main() -> None:
    app()


if __name__ == "__main__":
    main()
