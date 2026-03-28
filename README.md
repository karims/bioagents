# bioagents

**bioagents** is a lightweight, bio-inspired multi-agent reasoning framework where independent agents generate, debate, and converge on the best insights for a given task.

---

## TL;DR

- Give it an input, a task type, and an objective  
- Multiple agents propose ideas from different perspectives  
- Agents reinforce or challenge each other  
- Weak ideas fade, strong ones survive  
- Near-duplicates are merged  
- You get a clean, ranked set of insights  

👉 Think: *a small team of AI specialists reasoning together instead of a single model response*

---

## What it does

bioagents runs a **goal-directed swarm loop** over your input:

1. Agents generate hypotheses  
2. Agents support or contradict each other  
3. Confidence evolves over iterations  
4. Weak hypotheses decay and get pruned  
5. Similar ideas are merged  
6. Final outputs are ranked and returned  

---

## Example use cases

- Code review (bugs, performance, fixes)
- Product analysis (why users churn, what to improve)
- Document reasoning (risks, inconsistencies, actions)
- Strategy exploration (multiple approaches + tradeoffs)

---

## Quickstart

```bash
python -m pip install -e .

bioagents run demos/sample_task.json
bioagents run demos/document_task.json
bioagents run demos/sample_task.json --top-k 1
```

---

## Example: PR Review

#### Input

We give bioagents a code change (or PR description) and a goal.

Example task JSON:

```json
{
  "task_type": "pr_review",
  "data": "This PR loops over all users and accesses user.profile.email without checking if profile exists.",
  "objective": "identify the main risks and suggest the best improvement",
  "config": {
    "top_k": 2
  }
}
```

---

#### What each field means

* `task_type`
  The type of problem. This helps select relevant reasoning patterns.
  Examples: `pr_review`, `document_analysis`, `spreadsheet_analysis`

* `data`
  The actual input to analyze.
  This can be code, text, logs, or structured data.

* `objective`
  The goal for this run.
  This guides how agents reason and what they prioritize.

* `config.top_k`
  Number of final results to return after ranking.
  bioagents may generate many ideas internally, but only the top K are returned.

---

#### What happens internally

bioagents runs a small swarm of specialized agents:

* `bug_agent` -> looks for correctness issues
* `performance_agent` -> looks for inefficiencies
* `solution_agent` -> proposes fixes
* `strategy_agent` -> suggests better approaches
* `critic_agent` -> challenges weak ideas

They operate in steps:

1. Each agent proposes hypotheses
2. Agents reinforce or contradict each other
3. Weak ideas decay, strong ideas gain support
4. Similar ideas are merged (clustering)
5. Final results are ranked

This is a bio-inspired process: ideas compete and evolve.

---

#### Example output

```json
[
  {
    "text": "Implement null-safe access for user.profile.email.",
    "source": "solution_agent",
    "confidence": 0.53
  },
  {
    "text": "Accessing user.profile.email without checking if profile exists may cause a runtime error.",
    "source": "bug_agent",
    "confidence": 0.48
  }
]
```

---

#### Why this is useful

Instead of a single answer, you get:

* multiple perspectives (bugs, performance, strategy)
* ranked insights
* both problems and actionable fixes

This makes it useful for:

* PR reviews
* design analysis
* document reasoning
* exploratory problem solving

---

## Task format

```json
{
  "task_type": "pr_review",
  "data": "...",
  "objective": "identify the main risks and suggest the best improvement",
  "config": {
    "top_k": 2
  }
}
```

`task_type` influences which built-in agents are used by default. You can override that with `config.agents`.

---

## Docker

```bash
docker build -t bioagents .
docker run --rm bioagents
```

Using local Ollama from Docker (macOS/Windows):

```bash
docker run --rm \
  -e BIOAGENTS_LLM_PROVIDER=ollama \
  -e BIOAGENTS_OLLAMA_MODEL=llama3.1:8b \
  -e BIOAGENTS_OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  bioagents
```

---

## Environment variables

### Ollama

```bash
export BIOAGENTS_LLM_PROVIDER=ollama
export BIOAGENTS_OLLAMA_MODEL=llama3.1:8b
export BIOAGENTS_OLLAMA_BASE_URL=http://localhost:11434
```

### OpenAI-compatible

```bash
export BIOAGENTS_LLM_PROVIDER=openai-compatible
export BIOAGENTS_OPENAI_BASE_URL="https://api.openai.com/v1"
export BIOAGENTS_OPENAI_API_KEY="your-key"
export BIOAGENTS_OPENAI_MODEL="gpt-4o-mini"
```

---

## Development

```bash
python -m pip install -e '.[dev]'
pytest
```

---

## Runtime visibility

Each run prints the active mode, task type, objective, per-agent timings, and a short summary before the final JSON output, including formed clusters and final returned results. Local agents also show that they ran without an LLM call.

---

## Policies

bioagents supports pluggable swarm policies. The current `default` policy preserves today’s behavior, and `ant` now emphasizes reinforcement and convergence on repeated strong ideas. `bee` and `immune` are reserved for future variants.

---

## Core concepts

- **Agents** → different perspectives (bug, strategy, solution, etc.)
- **Skills** → capabilities agents can use (analyze, rewrite, evaluate)
- **Objective** → what the swarm is trying to solve
- **Blackboard** → shared space where ideas evolve
- **Rules** → reinforce, contradict, decay, prune
- **Clustering** → merge near-duplicate ideas before ranking

---

## Notes

- Provider failures fall back automatically for the current run  
- Similarity merging is heuristic (`difflib`) and intentionally conservative, not embedding-based  
- Skills are currently descriptive, not executable tools yet  
