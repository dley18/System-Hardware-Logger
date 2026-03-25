"""Load, VRAM, temp"""
import pynvml
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetName, nvmlDeviceGetMemoryInfo, nvmlDeviceGetTemperatureV, nvmlDeviceGetPowerUsage

from .base import BaseCollector

class GPUCollector(BaseCollector):

    def __init__(self) -> None:
        self.gpu_metrics = {}

    def collect(self) -> None:
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
                
                self.gpu_metrics[name] = data
        finally:
            nvmlShutdown()

    def get_gpu_metrics(self) -> dict:
        return self.gpu_metrics
