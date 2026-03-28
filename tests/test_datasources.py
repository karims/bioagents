from pathlib import Path

from bioagents.datasources.file import FileDataSource
from bioagents.datasources.github_pr import GitHubPRDataSource
from bioagents.datasources.registry import get_datasource, load_data
from bioagents.datasources.text import TextDataSource


def test_text_datasource_loads_content() -> None:
    datasource = TextDataSource()

    assert datasource.load({"content": "hello"}) == "hello"


def test_registry_load_data_uses_text_for_raw_strings() -> None:
    assert load_data("plain text input") == "plain text input"
    assert isinstance(get_datasource("text"), TextDataSource)


def test_file_datasource_loads_txt(tmp_path: Path) -> None:
    path = tmp_path / "note.txt"
    path.write_text("hello from file", encoding="utf-8")

    datasource = FileDataSource()

    assert datasource.load({"path": str(path)}) == "hello from file"


def test_github_pr_datasource_formats_diff(monkeypatch) -> None:
    class _Response:
        status_code = 200
        text = "diff --git a/app.py b/app.py\n+print('hello')\n"

    def fake_get(url: str, headers: dict[str, str], timeout: int):
        assert url == "https://api.github.com/repos/openai/bioagents/pulls/12"
        assert headers["Accept"] == "application/vnd.github.v3.diff"
        assert timeout == 10
        return _Response()

    monkeypatch.setattr("bioagents.datasources.github_pr.requests.get", fake_get)

    datasource = GitHubPRDataSource()
    text = datasource.load({"type": "github_pr", "repo": "openai/bioagents", "pr_number": 12})

    assert "=== FILE CHANGE ===" in text
    assert "print('hello')" in text
