"""Memory Metric Collector"""
import psutil
from .base import BaseCollector

class MemoryCollector(BaseCollector):
    """Memeory Metric Collector."""

    def __init__(self) -> None:
        self.memory_metrics = {}

    def collect(self) -> None:
        """Collects total RAM in GB, available RAM in GB, used RAM in GB, and RAM usage percentage."""

        memory = psutil.virtual_memory()
        self.memory_metrics["total_GB"] = round(int(memory.total) / 10**9, 3)
        self.memory_metrics["available_GB"] = round(int(memory.available) / 10**9, 3)
        self.memory_metrics["used_GB"] = round(int(memory.used) / 10**9, 3)
        self.memory_metrics["percent"] = memory.percent

    def get_memory_metrics(self) -> dict:
        """
        Returns:
            dict: Dictionary containing Memroy Metrics.
        """
        return self.memory_metrics