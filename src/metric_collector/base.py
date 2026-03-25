"""Base Collector Class."""

from abc import ABC, abstractmethod

class BaseCollector(ABC):
    """Base Collector Implementation."""

    @abstractmethod
    def collect(self) -> None:
        """Collect method to be implemented by children."""
        pass

    def collect_safe(self) -> None:
        """Handles all exceptions raised from collect()."""
        try:
            self.collect()
        except Exception as e:
            print(f"Error: {e}")