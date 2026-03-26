"""Builds payload data structure."""
import json
class Payload:
    """Payload data structure."""

    def __init__(self) -> None:
        self.payload = {}

    def build_payload(self, cpu, memory, disk, gpu, network, battery) -> dict:
        """
        Builds payload data structure.

        Parameters:
            cpu (dict): Dictionary containing CPU Metrics
            memory (dict): Dictionary containing Memory Metrics
            disk (dict): Dictionary containing Disk Metrics
            gpu (dict): Dictionary containing GPU Metrics
            network (dict): Dictionary containing Network Metrics
            battery (dict): Dictionary containing Battery Metrics

        Returns:
            dict: Currently returns data dictionary but this method will be deprecated.
        """
        self.payload["cpu"] = cpu
        self.payload["memory"] = memory
        self.payload["disk"] = disk
        self.payload["gpu"] = gpu
        self.payload["network"] = network
        self.payload["battery"] = battery

        return self.payload
    
    