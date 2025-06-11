import os
from configparser import ConfigParser

DEFAULT_CONFIG_PATH = "/etc/app/app.conf"


def load_config(path: str = DEFAULT_CONFIG_PATH) -> ConfigParser:
    """Return ConfigParser instance with Serverless' configuration."""

    if not os.path.exists(path):
        raise FileExistsError(f"Config file does not exist: {path}")
    config_parser = ConfigParser()
    config_parser.read(path)
    return config_parser
