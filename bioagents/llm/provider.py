import json
import os
from dataclasses import dataclass, field
from typing import Protocol
from urllib import request


class Provider(Protocol):
    mode_name: str

    def generate(self, prompt: str) -> str:
        ...


@dataclass
class OllamaProvider:
    model: str
    base_url: str = "http://localhost:11434"
    mode_name: str = field(default="ollama", init=False)

    def generate(self, prompt: str) -> str:
        body = json.dumps(
            {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            }
        ).encode("utf-8")
        req = request.Request(
            url=f"{self.base_url.rstrip('/')}/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return str(payload.get("response", "")).strip()


@dataclass
class OpenAICompatibleProvider:
    base_url: str
    api_key: str
    model: str
    mode_name: str = field(default="openai-compatible", init=False)

    def generate(self, prompt: str) -> str:
        body = json.dumps(
            {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
            }
        ).encode("utf-8")
        req = request.Request(
            url=f"{self.base_url.rstrip('/')}/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        choice = payload["choices"][0]
        message = choice.get("message", {})
        return str(message.get("content", "")).strip()


@dataclass
class MockProvider:
    response: str
    mode_name: str = field(default="mock", init=False)

    def generate(self, prompt: str) -> str:
        return self.response


def _get_env(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def get_provider_from_env() -> tuple[str, Provider | None]:
    provider_name = os.getenv("BIOAGENTS_LLM_PROVIDER", "").strip().lower()

    if provider_name == "ollama":
        model = _get_env("BIOAGENTS_OLLAMA_MODEL", "BIOAGENTS_LLM_MODEL")
        if not model:
            return "fallback", None
        base_url = _get_env("BIOAGENTS_OLLAMA_BASE_URL", "BIOAGENTS_LLM_BASE_URL")
        if not base_url:
            base_url = "http://localhost:11434"
        return "ollama", OllamaProvider(model=model, base_url=base_url)

    base_url = _get_env("BIOAGENTS_OPENAI_BASE_URL", "BIOAGENTS_LLM_BASE_URL")
    api_key = _get_env("BIOAGENTS_OPENAI_API_KEY", "BIOAGENTS_LLM_API_KEY")
    model = _get_env("BIOAGENTS_OPENAI_MODEL", "BIOAGENTS_LLM_MODEL")

    if not base_url or not api_key or not model:
        return "fallback", None

    return "openai", OpenAICompatibleProvider(
        base_url=base_url,
        api_key=api_key,
        model=model,
    )


def provider_from_env() -> Provider | None:
    _, provider = get_provider_from_env()
    return provider
