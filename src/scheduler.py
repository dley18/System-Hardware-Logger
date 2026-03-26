"""Metric Collection Scheduler"""

import time

from collector import Collector
from config_manager import ConfigManager
from payload import Payload
from database_manager import DatabaseManager

class Scheduler:
    """Metric Collection Scheduler."""

    def __init__(self) -> None:
        self._collector = Collector()
        self._config_mananger = ConfigManager()
        self._payload = Payload()
        self._config = None
        self._polling_interval = None
        self._sqlitedb = None
        self._database_manager = None


    def setup_application(self) -> None:
        print("*****#####----- System Hardware Logger -----#####*****")

        print("Loading configuration")
        self._config_mananger.parse_args()
        self._config = self._config_mananger.get_config()

        self._sqlitedb = self._config["sqlite_db"]
        self._database_manager = DatabaseManager(self._sqlitedb)
        self._polling_interval = self._config["interval"]

        # Create database table schema
        self._database_manager.create_table_schema()
        print("Configuration Loaded")

        print(f"Polling every {self._polling_interval} seconds")
        self._poll()


    def _poll(self) -> None:
        """Polling collection/logging loop that repeats at the given interval per second."""

        next_run = time.perf_counter()
        cpu = {}
        memory = {}
        disk = {}
        gpu = {}
        network = {}
        battery = {}
        
        while True:
            next_run += self._polling_interval

            if self._config["metrics"]["cpu"]:
                self._collector.collect_cpu_metrics()
                cpu = self._collector.get_cpu_metrics()

            if self._config["metrics"]["memory"]:
                self._collector.collect_memory_metrics()
                memory = self._collector.get_memory_metrics()

            if self._config["metrics"]["disk"]:
                self._collector.collect_disk_metrics()
                disk = self._collector.get_disk_metrics()

            if self._config["metrics"]["gpu"]:
                self._collector.collect_gpu_metrics()
                gpu = self._collector.get_gpu_metrics()

            if self._config["metrics"]["network"]:
                self._collector.collect_network_metrics()
                network = self._collector.get_network_metrics()

            if self._config["metrics"]["battery"]:
                self._collector.collect_battery_metrics()
                battery = self._collector.get_battery_metrics()

            payload = self._payload.build_payload(cpu, memory, disk, gpu, network, battery)
            self._database_manager.log_payload(payload)

            sleep_time = next_run - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)
    
