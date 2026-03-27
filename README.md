# bioagents

Minimal Python swarm runtime skeleton.

Hypotheses are structured objects with `text`, `source`, `confidence`, `support`, and `sources`.
Blackboard storage is separate from swarm rules.
Repeated hypotheses are reinforced by a local rule.
Confidence also decays over runtime steps, and weak hypotheses can be pruned.
This creates a minimal exploration versus stabilization loop while keeping future rules easy to add.

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
    "confidence": 0.64,
    "support": 3,
    "sources": ["bug_agent"]
  }
]
```
