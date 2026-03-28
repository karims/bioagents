# Bio-Inspired Policies in Multi-Agent Hypothesis Systems

This document explains the theoretical intuition behind three policies:

- AntPolicy (Ant Colony Optimization inspired)
- BeePolicy (Artificial Bee Colony inspired)
- ImmunePolicy (Artificial Immune System inspired)

These are not exact implementations of the classical algorithms, but **adaptations of their core ideas** into a hypothesis-ranking and multi-agent reasoning framework.

---

## 🐜 AntPolicy — Ant Colony Optimization (ACO)

### Core Idea (Theory)
In ACO:
- Ants explore paths randomly
- Good paths get reinforced via **pheromones**
- Pheromones **decay over time**
- Eventually, shortest/best paths dominate

### Mapping to Your System

| ACO Concept | Your System |
|------------|------------|
| Ants       | Agents generating hypotheses |
| Paths      | Hypotheses |
| Pheromone  | `trail_strength` |
| Reinforcement | `trail_increment` |
| Evaporation | `trail_decay` |
| Selection | `ranking_key` |

### Key Behavior in Code

- Every hypothesis starts with minimum trail strength:
```python
hypothesis.trail_strength = max(hypothesis.trail_strength, 0.12)
```

- Ranking prioritizes:
  1. Trail strength (collective belief)
  2. Confidence
  3. Support
  4. Low opposition

👉 This is **pure exploitation** — strongest hypotheses dominate over time.

### Interpretation

- System converges toward a few strong hypotheses
- Works well when signal is clean
- Weak when:
  - Data is noisy
  - Early wrong hypotheses get reinforced

---

## 🐝 BeePolicy — Artificial Bee Colony (ABC)

### Core Idea (Theory)
In ABC:
- **Scout bees** explore randomly (new food sources)
- **Worker bees** exploit known good sources
- **Onlooker bees** evaluate and select best sources

Balance:
👉 Exploration + Exploitation

### Mapping to Your System

| Bee Role | Your Agents |
|----------|------------|
| Scouts   | bug_agent, performance_agent, strategy_agent |
| Workers  | solution_agent |
| Critics  | critic_agent |

### Phase-Based Behavior

#### Exploration Phase (early steps)
- Scouts + critics active
- Boost novelty:
```python
hypothesis.novelty_score = max(hypothesis.novelty_score, 0.35)
```

#### Exploitation Phase (later steps)
- Workers + critics active
- Boost trail strength:
```python
hypothesis.trail_strength = max(hypothesis.trail_strength, 0.08)
```

### Ranking Strategy

```python
confidence + (novelty_score * 0.15)
```

👉 Hybrid scoring:
- Confidence (quality)
- Novelty (diversity)
- Support (agreement)

### Interpretation

- Early: explore many ideas
- Later: refine best ones
- More robust than AntPolicy

---

## 🧬 ImmunePolicy — Artificial Immune System (AIS)

### Core Idea (Theory)
Immune systems:
- Detect **anomalies (antigens)**
- Activate strong response to threats
- Suppress normal/background signals
- Build memory of dangerous patterns

### Mapping to Your System

| Immune Concept | Your System |
|---------------|------------|
| Antigens      | Bugs, anomalies |
| Antibodies    | Hypotheses |
| Detection     | anomaly_score |
| Response      | prioritization |
| Memory        | reinforcement over time |

### Key Behavior

- Certain agents increase anomaly score:
```python
hypothesis.anomaly_score = max(hypothesis.anomaly_score, 0.4)
```

- Strategy agent adds weaker signal:
```python
hypothesis.anomaly_score = max(hypothesis.anomaly_score, 0.15)
```

### Ranking Strategy

```python
(
    anomaly_score,
    confidence - (opposition * 0.08),
    support,
    -opposition
)
```

👉 Strong bias toward:
- High anomaly
- Low contradiction

### Interpretation

- Focuses on **finding what's wrong**
- Excellent for:
  - Debugging
  - Incident analysis
  - Root cause detection

- Weak for:
  - General reasoning
  - Creative exploration

---

## ⚖️ Comparison Summary

| Policy | Strength | Weakness | Use Case |
|--------|----------|----------|----------|
| Ant    | Strong convergence | Gets stuck early | Stable environments |
| Bee    | Balanced exploration | Slightly complex | General reasoning |
| Immune | Detects anomalies | Ignores normal cases | Debugging / RCA |

---

## 🧠 Final Insight

These policies are **search strategies over hypothesis space**:

- Ant → Reinforce what works
- Bee → Explore then refine
- Immune → Detect what’s wrong

👉 The key idea is not biology — it's:
> Different ways to navigate and rank competing hypotheses.

---
