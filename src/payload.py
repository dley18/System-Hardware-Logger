"""Builds json snapshot"""
import json
class PayloadBuilder:

    def __init__(self) -> None:
        self.payload = {}

    def build_payload(self, cpu, memory, disk, gpu, network, battery) -> dict:
        self.payload["cpu"] = cpu
        self.payload["memory"] = memory
        self.payload["disk"] = disk
        self.payload["gpu"] = gpu
        self.payload["network"] = network
        self.payload["battery"] = battery

        return self.payload
    
    