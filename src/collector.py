import psutil
from pynvml import *

class Collector:

    def __init__(self):
        self._cpu_metrics = {}
        self._memory_metrics = {}
        self._disk_metrics = {}
        self._gpu_metrics = {}
        self._network_metrics = {}
        self._battery_metrics = {}

    def collect_cpu_metrics(self) -> None:
        """Collects CPU Usage Percentage, per-core usage percentage, CPU Frequency, Number of Cores, and Number of Logical Cores."""

        self._cpu_metrics["cpu_percent"] = psutil.cpu_percent()
        self._cpu_metrics["per_core_percent"] = psutil.cpu_percent(percpu=True)
        self._cpu_metrics["cpu_freq"] = psutil.cpu_freq().current
        self._cpu_metrics["cpu_count"] = psutil.cpu_count()
        self._cpu_metrics["logical_cpu_count"] = psutil.cpu_count(logical=True)

    def get_cpu_metrics(self) -> dict:
        return self._cpu_metrics
    
    def collect_memory_metrics(self) -> None:
        """Collects total RAM in GB, available RAM in GB, used RAM in GB, and RAM usage percentage."""

        memory = psutil.virtual_memory()
        self._memory_metrics["total_GB"] = round(int(memory.total) / 10**9, 3)
        self._memory_metrics["available_GB"] = round(int(memory.available) / 10**9, 3)
        self._memory_metrics["used_GB"] = round(int(memory.used) / 10**9, 3)
        self._memory_metrics["percent"] = memory.percent

    def get_memory_metrics(self) -> dict:
        return self._memory_metrics
    
    def collect_disk_metrics(self) -> dict:
        """Collects the following metrics per interface: Total Storage in GB, Used Storage in GB, Free Storage in GB, and Usage Percentage."""

        disk_partitions = psutil.disk_partitions()
        for partition in disk_partitions:
            path = partition.mountpoint
            disk = psutil.disk_usage(path)

            data = {}
            data["total_GB"] = round(int(disk.total) / 10**9, 3)
            data["used_GB"] = round(int(disk.used) / 10**9, 3)
            data["free_GB"] = round(int(disk.free) / 10**9, 3)
            data["percent"] = disk.percent

            self._disk_metrics[path] = data

    def get_disk_metrics(self) -> dict:
        return self._disk_metrics
    
    def collect_gpu_metrics(self) -> None:
        """Collects the following metrics per NVIDIA GPU: 
        GPU Temperature, GPU Utilization Percentage, 
        GPU Memory Controller Utilization Percentage, 
        Total VRAM in GB, 
        Used VRAM in GB, 
        Free VRAM in GB, 
        and Power Usage.
        """
        nvmlInit()
        
        try:
            count = nvmlDeviceGetCount()
        
            for i in range(count):
                handle = nvmlDeviceGetHandleByIndex(i)
                name = nvmlDeviceGetName(handle)
                util = nvmlDeviceGetUtilizationRates(handle)
                mem = nvmlDeviceGetMemoryInfo(handle)

                data = {}
                data["temp"] = nvmlDeviceGetTemperatureV(handle, NVML_TEMPERATURE_GPU)
                data["util_percent"] = util.gpu
                data["mem_controller_util_percent"] = util.memory
                data["vram_total_GB"] = round(int(mem.total) / 10**9, 3)
                data["vram_used_GB"] = round(int(mem.used) / 10**9, 3)
                data["vram_free_GB"] = round(int(mem.free) / 10**9, 3)
                data["power_usage"] = round(nvmlDeviceGetPowerUsage(handle) / 1000, 3)
                
                self._gpu_metrics[name] = data
        finally:
            nvmlShutdown()

    def get_gpu_metrics(self) -> dict:
        return self._gpu_metrics
    
    def collect_network_metrics(self) -> None:
        """Collects the following per network interface: 
        Total GB sent, 
        Total GB recieved, 
        number of packets sent, 
        number of incoming errors, 
        number of outgoing errors, 
        number of incoming drops, 
        and the number of outgoing drops.
        """

        nics = psutil.net_io_counters(pernic=True)
        for entry in nics.items():
            name, stats = entry
            data = {}

            data["GB_sent"] = round(int(stats.bytes_sent) / 10**9, 3)
            data["GB_recv"] = round(int(stats.bytes_recv) / 10**9, 3)
            data["packets_sent"] = stats.packets_sent
            data["errors_in"] = stats.errin
            data["errors_out"] = stats.errout
            data["drops_in"] = stats.dropin
            data["drops_out"] = stats.dropout
            
            self._network_metrics[name] = data

    def get_network_metrics(self) -> dict:
        return self._network_metrics
    
    def collect_battery_metrics(self) -> None:
        """Collects battery percentage, seconds remaining, and if-charging."""

        battery = psutil.sensors_battery()
        self._battery_metrics["percent"] = battery.percent
        self._battery_metrics["secs_left"] = battery.secsleft
        self._battery_metrics["charging"] = battery.power_plugged

    def get_battery_metrics(self) -> dict:
        return self._battery_metrics