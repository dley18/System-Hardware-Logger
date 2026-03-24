"""Main entry point, argument parsing"""
from config_loader import ConfigLoader
from scheduler import Scheduler

def main():
    config_loader = ConfigLoader()
    config_loader.parse_args()
    config = config_loader.get_config()

    scheduler = Scheduler()
    scheduler.poll(5)
    


if __name__ == "__main__":
    main()
