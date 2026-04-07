import requests
from datetime import datetime
import socket
import json

class Poster:

    def __init__(self, url: str):
        "Posts metrics to Pulse WebApp"
        self._url = url

    def post_payload(self, payload: dict) -> None:
        """
        Posts snapshot of metrics to Pulse Server.
        
        Parameters:
            payload (dict): Payload of data
        """

        host_name = socket.gethostname()
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        snapshot_data = {"hostname": host_name, "timestamp": timestamp}
        snapshot_response = requests.post(self._url + "/snapshot", json=snapshot_data)
        snapshot_json = snapshot_response.json()
        print("DEBUG: Snapshot Response:", snapshot_json["ok"])
        snapshot_id = None
        if snapshot_json["ok"]:
            snapshot_id = int(snapshot_json["id"])
        else:
            return

        for key, value in payload.items():
            if key == "cpu" and payload["cpu"]:
                cpu_data = {
                    "snapshot_id": snapshot_id, 
                    "usage_percent": value["cpu_percent"],
                    "freq": value["cpu_freq"],
                    "temp": None,
                    "core_count": value["cpu_count"]
                }
                cpu_response = requests.post(self._url + "/cpu", json=cpu_data)
                cpu_json = cpu_response.json()
                print("DEBUG: CPU Response:", cpu_json["ok"])
            elif key == "memory" and payload["memory"]:
                memory_data = {
                    "snapshot_id": snapshot_id,
                    "ram_percent": value["percent"],
                    "ram_used_GB": value["used_GB"],
                    "ram_total_GB": value["total_GB"]
                }
                memory_response = requests.post(self._url + "/memory", json=memory_data)
                memory_json = memory_response.json()
                print("DEBUG: Memory Response:", memory_json["ok"])
            elif key == "disk" and payload["disk"]:
                for disk_name, disk_data in value.items():
                    per_disk_data = {
                        "snapshot_id": snapshot_id,
                        "mountpoint": disk_name,
                        "percent": disk_data["percent"],
                        "free_GB": disk_data["free_GB"],
                        "used_GB": disk_data["used_GB"],
                        "total_GB": disk_data["total_GB"]
                    }
                    disk_response = requests.post(self._url + "/disk", json=per_disk_data)
                    disk_json = disk_response.json()
                    print("DEBUG: Disk Response:", disk_json["ok"])
            elif key == "gpu" and payload["gpu"]:
                for gpu_name, gpu_data in value.items():
                    per_gpu_data = {
                        "snapshot_id": snapshot_id,
                        "gpu_name": gpu_name,
                        "utilization": gpu_data["util_percent"],
                        "vram_total_GB": gpu_data["vram_total_GB"],
                        "vram_used_GB": gpu_data["vram_used_GB"],
                        "vram_free_GB": gpu_data["vram_free_GB"],
                        "temp": gpu_data["temp"]
                    }
                    gpu_response = requests.post(self._url + "/gpu", json=per_gpu_data)
                    gpu_json = gpu_response.json()
                    print("DEBUG: GPU Response:", gpu_json["ok"])
            elif key == "network" and payload["network"]:
                for interface, interface_data in value.items():
                    per_interface_data = {
                        "snapshot_id": snapshot_id,
                        "network_interface": interface,
                        "GB_sent": interface_data["GB_sent"],
                        "GB_recv": interface_data["GB_recv"],
                        "packets_sent": interface_data["packets_sent"],
                        "errors_in": interface_data["errors_in"],
                        "errors_out": interface_data["errors_out"],
                        "drops_in": interface_data["drops_in"],
                        "drops_out": interface_data["drops_out"]
                    }
                    network_response = requests.post(self._url + "/network", json=per_interface_data)
                    network_json = network_response.json()
                    print("DEBUG: Network Response:", network_json["ok"])
            elif key == "battery" and payload["battery"]:
                battery_data = {
                    "snapshot_id": snapshot_id,
                    "percent": value["percent"],
                    "charging": True if value["charging"] == 1 else False,
                    "secs_left": value["secs_left"]
                }
                battery_response = requests.post(self._url + "/battery", json=battery_data)
                battery_json = battery_response.json()
                print("DEBUG: Battery Response:", battery_json["ok"])


