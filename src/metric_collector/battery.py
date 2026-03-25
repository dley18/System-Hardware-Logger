"""Battery Metrics Collector."""

import psutil

from .base import BaseCollector

class BatteryCollector(BaseCollector):
    """Battery Metrics Collector."""

    def __init__(self) -> None:
        self.battery_metrics = {}

    def collect(self) -> None:
        """Collects battery percentage, seconds remaining, and if-charging."""
        battery = psutil.sensors_battery()
        self.battery_metrics["percent"] = battery.percent
        self.battery_metrics["secs_left"] = battery.secsleft
        self.battery_metrics["charging"] = battery.power_plugged

    def get_battery_metrics(self) -> dict:
        """
        Returns:
            dict: Dictionary containing battery metrics
        """
        return self.battery_metrics