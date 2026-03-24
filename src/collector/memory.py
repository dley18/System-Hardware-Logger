"""Ram and Swap"""
import psutil
from .base import BaseCollector

class MemoryCollector(BaseCollector):

    def __init__(self) -> None:
        self.memory_metrics = {}

    def collect(self) -> None:
        memory = psutil.virtual_memory()
        self.memory_metrics["total"] = memory.total
        self.memory_metrics["available"] = memory.available
        self.memory_metrics["used"] = memory.used
        self.memory_metrics["percent"] = memory.percent

    def get_memory_metrics(self) -> dict:
        return self.memory_metrics