"""Main Application Entry Point."""
from scheduler import Scheduler

def main():
    """Main entry point for System Hardware Logger."""

    scheduler = Scheduler()
    scheduler.setup_application()
    
if __name__ == "__main__":
    main()
