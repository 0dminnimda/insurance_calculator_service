"""
Logging configs and utils
"""

from copy import deepcopy
from pathlib import Path
from typing import Dict

import uvicorn

from . import options

LOGFILE = Path(__file__).parent / "app.log"


def log_section_separator() -> None:
    if options.LOG_TO_FILE:
        LOGFILE.open(mode="a", encoding="utf-8").write("\n")


def file_logging_handler(formatter: str) -> Dict[str, str]:
    return {
        "formatter": formatter,
        "filename": str(LOGFILE),
        "class": "logging.FileHandler",
    }


def stdout_logging_handler(formatter: str) -> Dict[str, str]:
    return {
        "formatter": formatter,
        "stream": "ext://sys.stdout",
        "class": "logging.StreamHandler",
    }


def redirect_handler_to_file(config: dict, handler: str) -> None:
    config["handlers"][handler] = file_logging_handler(
        config["handlers"][handler]["formatter"]
    )


STDOUT_CONFIG: dict = deepcopy(uvicorn.config.LOGGING_CONFIG)
FILE_CONFIG: dict = deepcopy(STDOUT_CONFIG)

for handler in FILE_CONFIG["handlers"].keys():
    redirect_handler_to_file(FILE_CONFIG, handler)


def setup(name: str):
    STDOUT_CONFIG["handlers"][name] = stdout_logging_handler("default")
    FILE_CONFIG["handlers"][name] = file_logging_handler("default")

    STDOUT_CONFIG["loggers"][name] = FILE_CONFIG["loggers"][name] = {
        "handlers": [name],
        "level": "INFO",
    }


def get_config() -> dict:
    if options.LOG_TO_FILE:
        return FILE_CONFIG
    return STDOUT_CONFIG
