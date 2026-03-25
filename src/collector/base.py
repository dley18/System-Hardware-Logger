"""Base Collector Class"""

from abc import ABC, abstractmethod

class BaseCollector(ABC):

    @abstractmethod
    def collect(self) -> None:
        pass

    def collect_safe(self):
        try:
            self.collect()
        except Exception as e:
            return {
                "error": str(e),
                "collector": self.__class__.__name__,
                "type": type(e).__name__
            }