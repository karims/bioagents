# bioagents

Minimal Python swarm runtime skeleton.

Hypotheses are structured objects with `text`, `source`, `confidence`, `support`, and `sources`.
Blackboard storage is separate from swarm rules.
Repeated hypotheses are reinforced by a local rule.
Confidence also decays over runtime steps, and weak hypotheses can be pruned.
Hypotheses can also be challenged by critic agents, which lower confidence on targeted ideas.
This creates a minimal support-versus-opposition loop while keeping future rules easy to add.
The project also includes a small pytest-based test suite.

## Run

```bash
python -m pip install -e .
bioagents run demos/sample_task.json
```

## Test

```bash
python -m pip install -e .[dev]
pytest
```

Example output:

```json
[
  {
    "text": "possible bug",
    "source": "bug_agent",
    "confidence": 0.64,
    "support": 3,
    "sources": ["bug_agent"]
  }
]
```
