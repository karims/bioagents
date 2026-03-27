# bioagents

**bioagents** is a lightweight, bio-inspired multi-agent reasoning framework where independent agents generate, debate, and converge on the best insights for a given task.

---

## TL;DR

- Give it a task + objective  
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

## Core concepts

- **Agents** → different perspectives (bug, strategy, solution, etc.)
- **Skills** → capabilities agents can use (analyze, rewrite, evaluate)
- **Objective** → what the swarm is trying to solve
- **Blackboard** → shared space where ideas evolve
- **Rules** → reinforce, contradict, decay, prune
- **Clustering** → merge near-duplicate ideas before ranking

---

## Quickstart

```bash
python -m pip install -e '.[dev]'

bioagents run demos/sample_task.json
bioagents run demos/document_task.json
bioagents run demos/sample_task.json --top-k 1
```

---

## Task format

```json
{
  "input": "...",
  "objective": "identify main risks and suggest improvements",
  "config": {
    "top_k": 2
  }
}
```

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
  -e BIOAGENTS_LLM_MODEL=llama3.1:8b \
  -e BIOAGENTS_LLM_BASE_URL=http://host.docker.internal:11434 \
  bioagents
```

---

## Environment variables

### Ollama

```bash
export BIOAGENTS_LLM_PROVIDER=ollama
export BIOAGENTS_LLM_MODEL=llama3.1:8b
export BIOAGENTS_LLM_BASE_URL=http://localhost:11434
```

### OpenAI-compatible

```bash
export BIOAGENTS_LLM_BASE_URL="https://api.openai.com/v1"
export BIOAGENTS_LLM_API_KEY="your-key"
export BIOAGENTS_LLM_MODEL="gpt-4o-mini"
```

---

## Tests

```bash
pytest
```

---

## Notes

- Provider failures fall back automatically for the current run  
- Similarity merging is heuristic (`difflib`), not embedding-based  
- Skills are currently descriptive, not executable tools yet  
