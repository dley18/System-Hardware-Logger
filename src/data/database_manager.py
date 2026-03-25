"""Database Manager."""
import sqlite3

class DatabaseManager:
    """Manages Database Operations."""


    def __init__(self, sqlitedb="system-hardware-logger.db") -> None:
        self.conn = sqlite3.connect(sqlitedb)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.cursor = self.conn.cursor()

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

        self.cursor.executescript(SCHEMA)
        self.conn.close()