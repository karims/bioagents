# bioagents

Experimental hobby project for running a tiny multi-agent blackboard loop over text tasks.

Current capabilities:
- Task JSON with optional runtime config
- Built-in agents: `bug_agent`, `performance_agent`, `critic_agent`
- Built-in rules: `reinforce`, `contradict`, `decay`, `prune`
- Ranked final outputs with optional `--top-k`
- Ollama, OpenAI-compatible, or fallback mode
- Pytest test suite

## Quickstart

```bash
python -m pip install -e '.[dev]'
bioagents run demos/sample_task.json
bioagents run demos/document_task.json
bioagents run demos/sample_task.json --top-k 1
```

Task JSON may include a `config` block for agents, rules, `max_steps`, and `top_k`.
CLI `--top-k` overrides `config.top_k`.

## Docker

```bash
docker build -t bioagents .
docker run --rm bioagents
```

To use local Ollama from Docker on macOS/Windows:

```bash
docker run --rm -e BIOAGENTS_LLM_PROVIDER=ollama -e BIOAGENTS_LLM_MODEL=llama3.1:8b -e BIOAGENTS_LLM_BASE_URL=http://host.docker.internal:11434 bioagents
```

## Env Vars

Ollama:

```bash
export BIOAGENTS_LLM_PROVIDER=ollama
export BIOAGENTS_LLM_MODEL=llama3.1:8b
export BIOAGENTS_LLM_BASE_URL=http://localhost:11434
bioagents run demos/sample_task.json
```

OpenAI-compatible:

```bash
export BIOAGENTS_LLM_BASE_URL="https://api.openai.com/v1"
export BIOAGENTS_LLM_API_KEY="your-key"
export BIOAGENTS_LLM_MODEL="gpt-4o-mini"
bioagents run demos/sample_task.json
```

## Tests

```bash
pytest
```
