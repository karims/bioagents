from bioagents.datasources.base import DataSource


class TextDataSource(DataSource):
    def load(self, config: dict) -> str:
        return str(config.get("content", ""))
