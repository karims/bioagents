import json
import os
from dataclasses import dataclass
from typing import Protocol
from urllib import request


class Provider(Protocol):
    def generate(self, prompt: str) -> str:
        ...


@dataclass
class OllamaProvider:
    model: str
    base_url: str = "http://localhost:11434"

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

    def generate(self, prompt: str) -> str:
        return self.response


def get_provider_from_env() -> tuple[str, Provider | None]:
    provider_name = os.getenv("BIOAGENTS_LLM_PROVIDER", "").strip().lower()
    model = os.getenv("BIOAGENTS_LLM_MODEL")

    if provider_name == "ollama":
        if not model:
            return "fallback", None
        base_url = os.getenv("BIOAGENTS_LLM_BASE_URL", "http://localhost:11434")
        return "ollama", OllamaProvider(model=model, base_url=base_url)

    base_url = os.getenv("BIOAGENTS_LLM_BASE_URL")
    api_key = os.getenv("BIOAGENTS_LLM_API_KEY")

    if not base_url or not api_key or not model:
        return "fallback", None

    return "openai-compatible", OpenAICompatibleProvider(
        base_url=base_url,
        api_key=api_key,
        model=model,
    )


def provider_from_env() -> Provider | None:
    _, provider = get_provider_from_env()
    return provider
