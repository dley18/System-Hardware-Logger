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
            data["total"] = disk.total
            data["used"] = disk.used
            data["free"] = disk.free
            data["percent"] = disk.percent

            self.disk_metrics[path] = data
    
    def get_disk_metrics(self) -> dict:
        return self.disk_metrics