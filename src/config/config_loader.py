"""Config loader"""

import argparse
import json

class ConfigLoader:
    """Config Loader for config.json file"""

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
            with open("config/config.json", "r") as file:
                self.config = json.load(file)

            if self.args.config:
                self.config = json.load(self.args.config)
                return self.config
            
            if self.args.url:
                self.config["backend_url"] = self.args.url

            if self.args.alert_url:
                self.config["alert_url"] = self.args.alert_url

            if self.args.sqlite_db:
                self.config["sqlite_db"] = self.args.sqlite_db

            if self.args.interval:
                self.config["interval"] = self.args.interval

            if self.args.api_key:
                self.config["api_key"] = self.args.api_key

            return self.config
        
        except FileNotFoundError:
            print("No default config file exists.")
            return self.config
        except json.JSONDecodeError:
            print("Failed to decode JSON from default config file.")
            return self.config
