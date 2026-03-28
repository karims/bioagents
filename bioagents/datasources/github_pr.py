import os

import requests

from bioagents.datasources.base import DataSource


class GitHubPRDataSource(DataSource):
    def load(self, config: dict) -> str:
        repo = config["repo"]
        pr_number = config["pr_number"]
        url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
        headers = {"Accept": "application/vnd.github.v3.diff"}

        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch PR diff: {response.status_code}")
        return self._format_diff(response.text)

    def _format_diff(self, diff: str) -> str:
        cleaned: list[str] = []
        for line in diff.splitlines():
            if line.startswith("diff --git"):
                cleaned.append("")
                cleaned.append("=== FILE CHANGE ===")
            cleaned.append(line)
        return "\n".join(cleaned)
