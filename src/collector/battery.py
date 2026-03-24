"""Percent, plugged in, and time remaining"""

import psutil

from .base import BaseCollector

class BatteryCollector(BaseCollector):

    def __init__(self) -> None:
        self.battery_metrics = {}

    def collect(self) -> None:
        battery = psutil.sensors_battery()
        self.battery_metrics["percent"] = battery.percent
        self.battery_metrics["secs_left"] = battery.secsleft
        self.battery_metrics["charging"] = battery.power_plugged

    def get_battery_metrics(self) -> dict:
        return self.battery_metrics