from bioagents.cli.main import build_demo_agents
from bioagents.core.task import Task
from bioagents.llm.provider import MockProvider, OllamaProvider, get_provider_from_env, provider_from_env


def test_provider_from_env_returns_none_without_configuration(monkeypatch) -> None:
    monkeypatch.delenv("BIOAGENTS_LLM_PROVIDER", raising=False)
    monkeypatch.delenv("BIOAGENTS_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("BIOAGENTS_LLM_API_KEY", raising=False)
    monkeypatch.delenv("BIOAGENTS_LLM_MODEL", raising=False)

    assert provider_from_env() is None


def test_get_provider_from_env_selects_ollama(monkeypatch) -> None:
    monkeypatch.setenv("BIOAGENTS_LLM_PROVIDER", "ollama")
    monkeypatch.setenv("BIOAGENTS_LLM_MODEL", "llama3.1:8b")
    monkeypatch.delenv("BIOAGENTS_LLM_BASE_URL", raising=False)

    mode, provider = get_provider_from_env()

    assert mode == "ollama"
    assert isinstance(provider, OllamaProvider)
    assert provider.base_url == "http://localhost:11434"


def test_invalid_ollama_config_falls_back_cleanly(monkeypatch) -> None:
    monkeypatch.setenv("BIOAGENTS_LLM_PROVIDER", "ollama")
    monkeypatch.delenv("BIOAGENTS_LLM_MODEL", raising=False)

    mode, provider = get_provider_from_env()

    assert mode == "fallback"
    assert provider is None


def test_openai_compatible_mode_selected_when_configured(monkeypatch) -> None:
    monkeypatch.delenv("BIOAGENTS_LLM_PROVIDER", raising=False)
    monkeypatch.setenv("BIOAGENTS_LLM_BASE_URL", "https://api.example.com/v1")
    monkeypatch.setenv("BIOAGENTS_LLM_API_KEY", "test-key")
    monkeypatch.setenv("BIOAGENTS_LLM_MODEL", "test-model")

    mode, provider = get_provider_from_env()

    assert mode == "openai-compatible"
    assert provider is not None


def test_demo_agents_fallback_when_provider_is_unavailable() -> None:
    agents = build_demo_agents(provider=None)
    submissions = agents[0].act(Task(task_type="pr_review", data="x"), _EmptyBoard())

    assert submissions[0].hypothesis.text == "possible bug"


def test_demo_agents_use_provider_when_available() -> None:
    agents = build_demo_agents(provider=MockProvider("unsafe attribute access"))
    submissions = agents[0].act(Task(task_type="pr_review", data="x"), _EmptyBoard())

    assert submissions[0].hypothesis.text == "unsafe attribute access"


class _EmptyBoard:
    def get_all(self) -> list[object]:
        return []
