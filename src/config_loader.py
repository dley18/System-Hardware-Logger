"""Config loader (CLI Arguments + YAML file)"""

import argparse
import json

class ConfigLoader:

    def __init__(self):
        self._parser = argparse.ArgumentParser(prog="System Hardware Logger", description="TODO", epilog="TODO")
        self._arg_list = ["--config", "--url", "--alert-url", "--sqlite-db", "--interval", "--api-key"]
        self._add_args()

    def _add_args(self):
        for arg in self._arg_list:
            self._parser.add_argument(arg)

    def parse_args(self):
        self.args = self._parser.parse_args()
        # print(self.args.config, self.args.url, self.args.alert_url)

    def get_config(self) -> dict:
        try:
            with open("config.json", "r") as file:
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
        except json.JSONDecodeError:
            print("Failed to decode JSON from default config file.")
