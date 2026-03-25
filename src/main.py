"""Main Application Entry Point."""
from config.config_loader import ConfigLoader
from scheduler import Scheduler
from data.database_manager import DatabaseManager


def main():
    """Main entry point for System Hardware Logger."""
    config_loader = ConfigLoader()
    config_loader.parse_args()
    config = config_loader.get_config()

    db = DatabaseManager()
    db.create_table_schema()

    scheduler = Scheduler("../database/system-hardware-logger.db")
    scheduler.poll(1)
    
    
if __name__ == "__main__":
    main()
