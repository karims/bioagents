from abc import ABC, abstractmethod


class DataSource(ABC):
    @abstractmethod
    def load(self, config: dict) -> str:
        """Return normalized text for agents."""
