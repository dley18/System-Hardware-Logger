"""Disk usage"""
import psutil
from .base import BaseCollector

class DiskCollector(BaseCollector):

    def __init__(self) -> None:
        self.disk_metrics = {}

    def collect(self) -> None:
        disk_partitions = psutil.disk_partitions()
        for partition in disk_partitions:
            path = partition.mountpoint
            disk = psutil.disk_usage(path)

            data = {}
            data["total_GB"] = round(int(disk.total) / 10**9, 3)
            data["used_GB"] = round(int(disk.used) / 10**9, 3)
            data["free_GB"] = round(int(disk.free) / 10**9, 3)
            data["percent"] = disk.percent

            self.disk_metrics[path] = data
    
    def get_disk_metrics(self) -> dict:
        return self.disk_metrics