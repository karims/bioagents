# bioagents

Minimal Python swarm runtime skeleton.

Hypotheses are structured objects with `text`, `source`, `confidence`, `support`, and `sources`.
Repeated hypotheses are merged by normalized text, support is tracked, and confidence increases when the same idea reappears.

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
    "confidence": 0.7,
    "support": 3,
    "sources": ["bug_agent"]
  }
]
```
