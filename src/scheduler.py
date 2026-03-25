"""Metric Collection Scheduler"""

import time


from metric_collector.cpu import CPUCollector
from metric_collector.memory import MemoryCollector
from metric_collector.disk import DiskCollector
from metric_collector.gpu import GPUCollector
from metric_collector.network import NetworkCollector
from metric_collector.battery import BatteryCollector
from data.payload import Payload
from telemetry.database_logger import DatabaseLogger

class Scheduler:
    """Metric Collection Scheduler."""

    def __init__(self, sqlitedb) -> None:
        self.cpu_collector = CPUCollector()
        self.memory_collector = MemoryCollector()
        self.disk_collector = DiskCollector()
        self.gpu_collector = GPUCollector()
        self.network_collector = NetworkCollector()
        self.battery_collector = BatteryCollector()
        self.payload = Payload()
        self.sqlitedb = sqlitedb
        self.database_logger = DatabaseLogger(self.sqlitedb)

    def poll(self, interval) -> None:
        """
        Polling collection/logging loop that repeats at the given interval per second.

        Parameters:
            interval (int): Time between runs in seconds.
        """

        next_run = time.perf_counter()


        while True:
            next_run += interval

            self.cpu_collector.collect_safe()
            cpu = self.cpu_collector.get_cpu_metrics()

            self.memory_collector.collect_safe()
            memory = self.memory_collector.get_memory_metrics()

            self.disk_collector.collect_safe()
            disk = self.disk_collector.get_disk_metrics()

            self.gpu_collector.collect_safe()
            gpu = self.gpu_collector.get_gpu_metrics()

            self.network_collector.collect_safe()
            network = self.network_collector.get_network_metrics()

            self.battery_collector.collect_safe()
            battery = self.battery_collector.get_battery_metrics()

            self.database_logger.log_payload(self.payload.build_payload(cpu, memory, disk, gpu, network, battery))

            sleep_time = next_run - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)
    
