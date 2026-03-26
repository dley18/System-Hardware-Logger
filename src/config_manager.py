"""Config manager"""

import argparse
import json

class ConfigManager:
    """Config manager for config.json file"""

    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(prog="System Hardware Logger", description="TODO", epilog="TODO")
        self._arg_list = ["--config", "--url", "--alert-url", "--sqlite-db", "--interval", "--api-key"]
        self._add_args()

    def _add_args(self) -> None:
        """Helper method to add CL args to Arg List."""

        for arg in self._arg_list:
            self._parser.add_argument(arg)

    def parse_args(self) -> None:
        """Parses CL arguments."""

        self.args = self._parser.parse_args()

    def get_config(self) -> dict:
        """
        Overrides default configuration file with CL arguments.

        Returns:
            dict: Dictionary containing app configuration.
        """

        try:
            config = None
            with open("config.json", "r") as file:
                config = json.load(file)

            if self.args.config:
                print(f"- Config file set to {self.args.config}")
                config = json.load(self.args.config)
                return config
            
            if self.args.url:
                print(f"- Setting backend url as {self.args.url}")
                config["backend_url"] = self.args.url

            if self.args.alert_url:
                print(f"- Setting alert url as {self.args.alert_url}")
                config["alert_url"] = self.args.alert_url

            if self.args.sqlite_db:
                print(f"- Setting {self.args.sqlite_db} as database location")
                config["sqlite_db"] = self.args.sqlite_db

            if self.args.interval:
                print(f"- Setting polling interval to {self.args.interval}")
                config["interval"] = self.args.interval

            if self.args.api_key:
                config["api_key"] = self.args.api_key

            return config
        
        except FileNotFoundError:
            print("No default config file exists.")
            return config
        except json.JSONDecodeError:
            print("Failed to decode JSON from default config file.")
            return config
