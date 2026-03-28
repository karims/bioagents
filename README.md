
# BioAgents

**BioAgents** is a bio-inspired multi-agent reasoning framework where specialized agents collaborate, compete, and converge on the best insights for a given task.

Instead of a single LLM response, BioAgents simulates a **team of reasoning agents** that generate, debate, and refine ideas.

---

# 🧠 TL;DR

- Provide input + objective  
- Multiple agents generate hypotheses  
- Agents reinforce or challenge each other  
- Weak ideas decay, strong ones survive  
- Similar ideas are merged  
- You get a ranked set of insights  

👉 Think: *a team of AI specialists reasoning together*

---

# ⚡ Why BioAgents?

Most AI systems:
- produce a **single answer**
- hide reasoning
- miss alternative perspectives

BioAgents:
- explores **multiple competing hypotheses**
- exposes **reasoning dynamics**
- produces **ranked, structured outputs**

---

# 🧩 How it works

BioAgents runs a **swarm loop over hypotheses**:

1. Agents generate ideas (hypotheses)  
2. Agents support or contradict each other  
3. Confidence evolves over iterations  
4. Weak ideas decay and get pruned  
5. Similar ideas are merged  
6. Final outputs are ranked  

---

# 🧪 Example: PR Review (Detailed)

## Input

```json
{
  "task_type": "pr_review",
  "data": "This PR loops over all users and accesses user.profile.email without checking if profile exists. It also performs a DB query inside the loop.",
  "objective": "identify risks and suggest improvements",
  "config": {
    "top_k": 3
  }
}
```

---

## Internal hypothesis evolution (simplified)

### Step 1 (generation)
- bug_agent → "Possible null access on user.profile"
- performance_agent → "N+1 query pattern due to DB call inside loop"
- solution_agent → "Add null check before accessing profile"
- strategy_agent → "Batch fetch profiles before loop"

### Step 2 (interaction)
- critic_agent rejects weak wording
- performance_agent reinforces N+1 issue
- strategy_agent supports batching approach

### Step 3 (refinement)
- duplicate ideas merged
- weak hypotheses decay
- strong ones accumulate support

---

## Final Output

```json
[
  {
    "text": "Database query inside loop creates N+1 performance issue; batch fetch profiles instead.",
    "source": "performance_agent",
    "confidence": 0.61
  },
  {
    "text": "Accessing user.profile.email without null check may cause runtime errors.",
    "source": "bug_agent",
    "confidence": 0.55
  },
  {
    "text": "Refactor loop to prefetch related data and add null-safe access.",
    "source": "solution_agent",
    "confidence": 0.52
  }
]
```

---

# 🤔 Why not just use GPT?

You could ask a single LLM:

> "Review this PR"

But that has limitations:

### ❌ Single-shot reasoning
- One answer
- No internal competition
- No refinement

### ❌ Hidden tradeoffs
- Doesn’t show alternatives
- No explicit disagreement

### ❌ No structured evolution
- No reinforcement or decay
- No idea merging

---

### ✅ What BioAgents does differently

- Generates **multiple competing hypotheses**
- Forces **agents to challenge each other**
- Uses **rules (reinforce / contradict / decay / prune)**
- Produces **ranked outputs instead of one answer**

👉 It turns reasoning into a **search problem over ideas**

---

# 🧠 Task Format

```json
{
  "task_type": "pr_review",
  "data": "...",
  "objective": "...",
  "config": {
    "top_k": 2
  }
}
```

---

# 🧬 Policies

| Policy  | Behavior |
|--------|--------|
| default | Balanced |
| ant     | Convergence |
| bee     | Explore → refine |
| immune  | Anomaly detection |

```bash
bioagents run demos/sample_task.json --policy bee
```

---

# 🧱 Core Concepts

- Agents → reasoning roles  
- Hypotheses → competing ideas  
- Blackboard → shared state  
- Rules → reinforce / contradict / decay / prune  
- Clustering → merge duplicates  

---

# 🚀 Quickstart

```bash
python -m pip install -e .

bioagents run demos/sample_task.json
bioagents run demos/sample_task.json --policy bee
```

---

# 🧪 Development

```bash
python -m pip install -e '.[dev]'
pytest
```

---

# 🔭 Roadmap

- Action agents (code edits)
- Better clustering
- More policies
- Visualization of reasoning

---

# ⚠️ Notes

- LLM fallback enabled  
- Clustering is heuristic  
- Agents reason, not act (yet)  

---

# 🧠 Final Thought

BioAgents is **not about generating answers**.

It is about:
👉 **evolving the best answer through competition**.
