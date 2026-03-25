"""Console + SQLite local file logging"""

import sqlite3
import time
import socket 

class Logger:

    def __init__(self, sqlitedb) -> None:
        self.sqlitedb = sqlitedb

    def log_payload(self, data) -> None:
        conn = sqlite3.connect(self.sqlitedb)
        cursor = conn.cursor()
        snapshot_query = "INSERT INTO Snapshots (hostname, timestamp) VALUES (?, ?)"
        host_name = socket.gethostname()
        timestamp = time.time()
        cursor.execute(snapshot_query, (host_name, timestamp))
        snapshot_id = cursor.lastrowid

        for key, value in data.items():
            if key == "cpu" and data["cpu"]:
                query = "INSERT INTO cpu_metrics (snapshot_id, usage_percent, freq, core_count) VALUES (?, ?, ?, ?)"
                cpu_metrics = (snapshot_id, value["cpu_percent"], value["cpu_freq"], value["cpu_count"])
                cursor.execute(query, cpu_metrics)
                print("Logged CPU")
            
            elif key == "memory" and data["memory"]:
                query = "INSERT INTO memory_metrics (snapshot_id, ram_percent, ram_used_GB, ram_total_GB) VALUES (?, ?, ?, ?)"
                memory_metrics = (snapshot_id, value["percent"], value["used_GB"], value["total_GB"])
                cursor.execute(query, memory_metrics)
                print("Logged memory")

            elif key == "disk" and data["disk"]:
                for disk_name, disk_data in value.items():
                    query = "INSERT INTO disk_metrics (snapshot_id, mountpoint, percent, free_GB, used_GB, total_GB) VALUES (?, ?, ?, ?, ?, ?)"
                    disk_metrics = (snapshot_id, disk_name, disk_data["percent"], disk_data["free_GB"], disk_data["used_GB"], disk_data["total_GB"])
                    cursor.execute(query, disk_metrics)
                    print("Logged disk")

            elif key == "gpu" and data["gpu"]:
                for gpu_name, gpu_data in value.items():
                    query = "INSERT INTO gpu_metrics (snapshot_id, gpu_name, utilization, vram_total_GB, vram_used_GB, vram_free_GB, temp) VALUES (?, ?, ?, ?, ?, ?, ?)"
                    gpu_metrics = (snapshot_id, gpu_name, gpu_data["util_percent"], gpu_data["vram_total_GB"], gpu_data["vram_used_GB"], gpu_data["vram_free_GB"], gpu_data["temp"])
                    cursor.execute(query, gpu_metrics)
                    print("Logged GPU")

            elif key == "network" and data["network"]:
                for interface, interface_data in value.items():
                    query = "INSERT INTO network_metrics (snapshot_id, interface, GB_sent, GB_recv, packets_sent, errors_in, errors_out, drops_in, drops_out) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                    network_metrics = (snapshot_id, interface, interface_data["GB_sent"], interface_data["GB_recv"], interface_data["packets_sent"], interface_data["errors_in"], interface_data["errors_out"], interface_data["drops_in"], interface_data["drops_out"])
                    cursor.execute(query, network_metrics)
                    print("Logged network")

            elif key == "battery" and data["battery"]:
                query = "INSERT INTO battery_metrics (snapshot_id, percent, charging, secs_left) VALUES (?, ?, ?, ?)"
                battery_metrics = (snapshot_id, value["percent"], value["charging"], value["secs_left"])
                cursor.execute(query, battery_metrics)
                print("Logged battery")

        conn.commit()
        conn.close()
            