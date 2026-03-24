"""Base Collector Class"""

from abc import ABC, abstractmethod

class BaseCollector(ABC):

    @abstractmethod
    def collect(self) -> dict:
        pass

    def collect_safe(self) -> dict:
        try:
            return self.collect()
        except Exception as e:
            return {
                "error": str(e),
                "collector": self.__class__.__name__,
                "type": type(e).__name__
            }