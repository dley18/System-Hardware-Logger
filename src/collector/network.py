"""Bytes, packets sent and recieved"""
import psutil

from .base import BaseCollector

class NetworkCollector(BaseCollector):

    def __init__(self) -> None:
        self.network_metrics = {}

    def collect(self) -> None:
        nics = psutil.net_io_counters(pernic=True)
        for entry in nics.items():
            name, stats = entry
            data = {}

            data["bytes_sent"] = stats.bytes_sent
            data["bytes_recv"] = stats.bytes_recv
            data["packets_sent"] = stats.packets_sent
            data["errors_in"] = stats.errin
            data["errors_out"] = stats.errout
            data["drops_in"] = stats.dropin
            data["drops_out"] = stats.dropout
            
            self.network_metrics[name] = data

    def get_network_metrics(self) -> dict:
        return self.network_metrics