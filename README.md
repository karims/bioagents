# bioagents

Minimal Python swarm runtime skeleton.

Hypotheses are structured objects with `text`, `source`, `confidence`, `support`, and `sources`.
Blackboard storage is separate from swarm rules.
Repeated hypotheses are merged by normalized text, and reinforcement is handled by a local rule so future rules like decay or pruning can be added cleanly.

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
