"""Network Metric Collector."""
import psutil

from .base import BaseCollector

class NetworkCollector(BaseCollector):
    """Network Metric Collector."""

    def __init__(self) -> None:
        self.network_metrics = {}

    def collect(self) -> None:
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
            
            self.network_metrics[name] = data

    def get_network_metrics(self) -> dict:
        """
        Returns:
            dict: Dictionary containing Network Metrics.
        """
        return self.network_metrics