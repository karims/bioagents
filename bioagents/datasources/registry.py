from typing import Any

from bioagents.datasources.file import FileDataSource
from bioagents.datasources.github_pr import GitHubPRDataSource
from bioagents.datasources.text import TextDataSource

_DATASOURCES = {
    "text": TextDataSource(),
    "file": FileDataSource(),
    "github_pr": GitHubPRDataSource(),
}


def get_datasource(name: str):
    if name not in _DATASOURCES:
        raise ValueError(f"Unknown datasource: {name}")
    return _DATASOURCES[name]


def load_data(data_config: str | dict[str, Any]) -> str:
    if isinstance(data_config, str):
        return get_datasource("text").load({"content": data_config})

    datasource = get_datasource(str(data_config.get("type", "text")))
    return datasource.load(data_config)
