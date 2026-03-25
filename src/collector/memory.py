"""Ram and Swap"""
import psutil
from .base import BaseCollector

class MemoryCollector(BaseCollector):

    def __init__(self) -> None:
        self.memory_metrics = {}

    def collect(self) -> None:
        memory = psutil.virtual_memory()
        self.memory_metrics["total_GB"] = round(int(memory.total) / 10**9, 3)
        self.memory_metrics["available_GB"] = round(int(memory.available) / 10**9, 3)
        self.memory_metrics["used_GB"] = round(int(memory.used) / 10**9, 3)
        self.memory_metrics["percent"] = memory.percent

    def get_memory_metrics(self) -> dict:
        return self.memory_metrics