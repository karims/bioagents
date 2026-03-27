from bioagents.core.registry import get_agent, get_agents
from bioagents.core.skills import get_skill_description
from bioagents.core.task import Task
from bioagents.llm.prompts import build_bug_prompt
from bioagents.llm.provider import MockProvider, OllamaProvider, get_provider_from_env, provider_from_env


def test_provider_from_env_returns_none_without_configuration(monkeypatch) -> None:
    monkeypatch.delenv("BIOAGENTS_LLM_PROVIDER", raising=False)
    monkeypatch.delenv("BIOAGENTS_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("BIOAGENTS_LLM_API_KEY", raising=False)
    monkeypatch.delenv("BIOAGENTS_LLM_MODEL", raising=False)
    monkeypatch.delenv("BIOAGENTS_OLLAMA_MODEL", raising=False)
    monkeypatch.delenv("BIOAGENTS_OLLAMA_BASE_URL", raising=False)
    monkeypatch.delenv("BIOAGENTS_OPENAI_BASE_URL", raising=False)
    monkeypatch.delenv("BIOAGENTS_OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("BIOAGENTS_OPENAI_MODEL", raising=False)

    assert provider_from_env() is None


def test_get_provider_from_env_selects_ollama(monkeypatch) -> None:
    monkeypatch.setenv("BIOAGENTS_LLM_PROVIDER", "ollama")
    monkeypatch.setenv("BIOAGENTS_OLLAMA_MODEL", "llama3.1:8b")
    monkeypatch.delenv("BIOAGENTS_OLLAMA_BASE_URL", raising=False)

    mode, provider = get_provider_from_env()

    assert mode == "ollama"
    assert isinstance(provider, OllamaProvider)
    assert provider.base_url == "http://localhost:11434"


def test_invalid_ollama_config_falls_back_cleanly(monkeypatch) -> None:
    monkeypatch.setenv("BIOAGENTS_LLM_PROVIDER", "ollama")
    monkeypatch.delenv("BIOAGENTS_OLLAMA_MODEL", raising=False)

    mode, provider = get_provider_from_env()

    assert mode == "fallback"
    assert provider is None


def test_openai_compatible_mode_selected_when_configured(monkeypatch) -> None:
    monkeypatch.setenv("BIOAGENTS_LLM_PROVIDER", "openai-compatible")
    monkeypatch.setenv("BIOAGENTS_OPENAI_BASE_URL", "https://api.example.com/v1")
    monkeypatch.setenv("BIOAGENTS_OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("BIOAGENTS_OPENAI_MODEL", "test-model")

    mode, provider = get_provider_from_env()

    assert mode == "openai-compatible"
    assert provider is not None


def test_legacy_env_vars_still_work(monkeypatch) -> None:
    monkeypatch.delenv("BIOAGENTS_LLM_PROVIDER", raising=False)
    monkeypatch.setenv("BIOAGENTS_LLM_BASE_URL", "https://api.example.com/v1")
    monkeypatch.setenv("BIOAGENTS_LLM_API_KEY", "test-key")
    monkeypatch.setenv("BIOAGENTS_LLM_MODEL", "test-model")

    mode, provider = get_provider_from_env()

    assert mode == "openai-compatible"
    assert provider is not None


def test_demo_agents_fallback_when_provider_is_unavailable() -> None:
    agents = get_agents(None, provider=None)
    submissions = agents[0].act(Task(task_type="pr_review", data="x"), _EmptyBoard())

    assert submissions[0].hypothesis.text == "possible bug"


def test_demo_agents_use_provider_when_available() -> None:
    agents = get_agents(None, provider=MockProvider("unsafe attribute access"))
    submissions = agents[0].act(Task(task_type="pr_review", data="x"), _EmptyBoard())

    assert submissions[0].hypothesis.text == "unsafe attribute access"


def test_provider_failure_surfaces_warning_and_falls_back_cleanly(capsys) -> None:
    agents = get_agents(None, provider=_FailingProvider())

    submissions = agents[0].act(Task(task_type="pr_review", data="x"), _EmptyBoard())

    captured = capsys.readouterr()
    assert "provider_warning=ollama generation failed; using fallback" in captured.err
    assert submissions[0].hypothesis.text == "possible bug"


def test_prompts_request_short_plain_output() -> None:
    bug_agent = get_agent("bug_agent", provider=None)
    prompt = build_bug_prompt(
        Task(task_type="pr_review", data="x"),
        _EmptyBoard(),
        bug_agent.skills,
        [get_skill_description(skill) for skill in bug_agent.skills],
    )

    assert "exactly one short plain sentence" in prompt
    assert "No markdown, bullets, code, explanation, or quotes." in prompt


def test_agent_cleans_generated_text() -> None:
    agents = get_agents(None, provider=MockProvider('"Unsafe access."\nExtra detail'))

    submissions = agents[0].act(Task(task_type="pr_review", data="x"), _EmptyBoard())

    assert submissions[0].hypothesis.text == "Unsafe access."


class _EmptyBoard:
    def get_all(self) -> list[object]:
        return []


class _FailingProvider:
    mode_name = "ollama"

    def generate(self, prompt: str) -> str:
        raise RuntimeError("boom")
