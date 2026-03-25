"""Console + SQLite local file logging"""

import sqlite3
class Logger:

    def __init__(self) -> None:
        pass

    def log_payload(self, data, sqlitedb) -> None:
        conn = sqlite3.connect(sqlitedb)
        cursor = conn.cursor()

        for key, value in data.items():
            if key == "cpu":
                pass
            
            elif key == "memory":
                pass

            elif key == "disk":
                pass

            elif key == "gpu":
                pass

            elif key == "network":
                pass

            elif key == "battery":
                pass
            