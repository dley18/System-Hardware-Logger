"""Database Manager."""
import sqlite3
import socket
import time
from contextlib import contextmanager

class DatabaseManager:
    """Manages Database Operations."""

    def __init__(self, sqlitedb="system-hardware-logger.db"):
        self.sqlitedb = sqlitedb

    @contextmanager
    def _get_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.sqlitedb)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def create_table_schema(self) -> None:
        """Creates database table schema in an SQLite Database file."""

        SCHEMA = """
        CREATE TABLE IF NOT EXISTS Snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostname TEXT NOT NULL,
            timestamp TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS cpu_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER,
            usage_percent REAL,
            freq REAL,
            temp REAL,
            core_count INTEGER,
            FOREIGN KEY (snapshot_id) REFERENCES Snapshots(id)
        );

        CREATE TABLE IF NOT EXISTS memory_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER,
            ram_percent REAL,
            ram_used_GB REAL,
            ram_total_GB REAL,
            FOREIGN KEY (snapshot_id) REFERENCES Snapshots(id)
        );

        CREATE TABLE IF NOT EXISTS gpu_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER,
            gpu_name TEXT,
            utilization REAL,
            vram_total_GB REAL,
            vram_used_GB REAL,
            vram_free_GB REAL,
            temp REAL,
            FOREIGN KEY (snapshot_id) REFERENCES Snapshots(id)
        );

        CREATE TABLE IF NOT EXISTS battery_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER,
            percent REAL,
            charging INTEGER,
            secs_left INTEGER,
            FOREIGN KEY (snapshot_id) REFERENCES Snapshots(id)
        );

        CREATE TABLE IF NOT EXISTS disk_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER,
            mountpoint TEXT,
            percent REAL,
            free_GB REAL,
            used_GB REAL,
            total_GB REAL,
            FOREIGN KEY (snapshot_id) REFERENCES Snapshots(id)
        );

        CREATE TABLE IF NOT EXISTS network_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER,
            interface TEXT,
            GB_sent REAL,
            GB_recv REAL,
            packets_sent INTEGER,
            errors_in INTEGER,
            errors_out INTEGER,
            drops_in INTEGER,
            drops_out INTEGER,
            FOREIGN KEY (snapshot_id) REFERENCES Snapshots(id)
        );
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.executescript(SCHEMA)

    def log_payload(self, data) -> None:
        """
        Logs a snapshot of data to the SQLite Database.

        Parameters:
            data (dict): Payload data.
        """


        with self._get_connection() as conn:
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
                    # print("DEBUG: Logged CPU")
                
                elif key == "memory" and data["memory"]:
                    query = "INSERT INTO memory_metrics (snapshot_id, ram_percent, ram_used_GB, ram_total_GB) VALUES (?, ?, ?, ?)"
                    memory_metrics = (snapshot_id, value["percent"], value["used_GB"], value["total_GB"])
                    cursor.execute(query, memory_metrics)
                    # print("DEBUG: Logged memory")

                elif key == "disk" and data["disk"]:
                    for disk_name, disk_data in value.items():
                        query = "INSERT INTO disk_metrics (snapshot_id, mountpoint, percent, free_GB, used_GB, total_GB) VALUES (?, ?, ?, ?, ?, ?)"
                        disk_metrics = (snapshot_id, disk_name, disk_data["percent"], disk_data["free_GB"], disk_data["used_GB"], disk_data["total_GB"])
                        cursor.execute(query, disk_metrics)
                    # print("DEBUG: Logged disk")

                elif key == "gpu" and data["gpu"]:
                    for gpu_name, gpu_data in value.items():
                        query = "INSERT INTO gpu_metrics (snapshot_id, gpu_name, utilization, vram_total_GB, vram_used_GB, vram_free_GB, temp) VALUES (?, ?, ?, ?, ?, ?, ?)"
                        gpu_metrics = (snapshot_id, gpu_name, gpu_data["util_percent"], gpu_data["vram_total_GB"], gpu_data["vram_used_GB"], gpu_data["vram_free_GB"], gpu_data["temp"])
                        cursor.execute(query, gpu_metrics)
                    # print("DEBUG: Logged GPU")

                elif key == "network" and data["network"]:
                    for interface, interface_data in value.items():
                        query = "INSERT INTO network_metrics (snapshot_id, interface, GB_sent, GB_recv, packets_sent, errors_in, errors_out, drops_in, drops_out) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                        network_metrics = (snapshot_id, interface, interface_data["GB_sent"], interface_data["GB_recv"], interface_data["packets_sent"], interface_data["errors_in"], interface_data["errors_out"], interface_data["drops_in"], interface_data["drops_out"])
                        cursor.execute(query, network_metrics)
                    # print("DEBUG: Logged network")

                elif key == "battery" and data["battery"]:
                    query = "INSERT INTO battery_metrics (snapshot_id, percent, charging, secs_left) VALUES (?, ?, ?, ?)"
                    battery_metrics = (snapshot_id, value["percent"], value["charging"], value["secs_left"])
                    cursor.execute(query, battery_metrics)
                    # print("DEBUG: Logged battery")
                
                conn.commit()
