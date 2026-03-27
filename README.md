# bioagents

Minimal Python swarm runtime skeleton.

Hypotheses are structured objects with `text`, `source`, and `confidence`.

## Run

```bash
python -m pip install -e .
bioagents run demos/sample_task.json
```

Example output:

```json
[
  {
    "text": "possible bug",
    "source": "bug_agent",
    "confidence": 0.6
  }
]
```
