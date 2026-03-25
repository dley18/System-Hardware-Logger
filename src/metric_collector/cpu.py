"""CPU Metric Collector."""
import psutil
from .base import BaseCollector

class CPUCollector(BaseCollector):
    """CPU Metric Collector."""

    def __init__(self) -> None:
        self.cpu_metrics = {}

    def collect(self) -> None:
        """Collects CPU Usage Percentage, per-core usage percentage, CPU Frequency, Number of Cores, and Number of Logical Cores."""
        self.cpu_metrics["cpu_percent"] = psutil.cpu_percent()
        self.cpu_metrics["per_core_percent"] = psutil.cpu_percent(percpu=True)
        self.cpu_metrics["cpu_freq"] = psutil.cpu_freq().current
        self.cpu_metrics["cpu_count"] = psutil.cpu_count()
        self.cpu_metrics["logical_cpu_count"] = psutil.cpu_count(logical=True)

    def get_cpu_metrics(self) -> dict:
        """
        Returns:
            dict: Dictionary containing cpu metrics.
        """
        return self.cpu_metrics