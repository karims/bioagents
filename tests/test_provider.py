from bioagents.cli.main import build_demo_agents
from bioagents.llm.provider import MockProvider, provider_from_env


def test_provider_from_env_returns_none_without_configuration(monkeypatch) -> None:
    monkeypatch.delenv("BIOAGENTS_LLM_BASE_URL", raising=False)
    monkeypatch.delenv("BIOAGENTS_LLM_API_KEY", raising=False)
    monkeypatch.delenv("BIOAGENTS_LLM_MODEL", raising=False)

    assert provider_from_env() is None


def test_demo_agents_fallback_when_provider_is_unavailable() -> None:
    agents = build_demo_agents(provider=None)
    submissions = agents[0].act({"task": "pr_review", "data": "x"}, _EmptyBoard())

    assert submissions[0].hypothesis.text == "possible bug"


def test_demo_agents_use_provider_when_available() -> None:
    agents = build_demo_agents(provider=MockProvider("unsafe attribute access"))
    submissions = agents[0].act({"task": "pr_review", "data": "x"}, _EmptyBoard())

    assert submissions[0].hypothesis.text == "unsafe attribute access"


class _EmptyBoard:
    def get_all(self) -> list[object]:
        return []
