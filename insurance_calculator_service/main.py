"""
Command line interface for the application and application entry point
"""

import argparse
import sys
from pathlib import Path

import uvicorn

# uvicorn requires absolute imports
from insurance_calculator_service import logger, options
from insurance_calculator_service.routes import app  # for uvicorn.run


def run(host: str = "localhost") -> None:
    logger.log_section_separator()

    file = Path(__file__)
    uvicorn.run(
        f"{file.stem}:app",
        app_dir=str(file.parent.absolute()),
        host=host,
        port=80,
        reload=options.RELOAD,
        log_level="info",
        log_config=logger.get_config(),
        use_colors=options.DEV_MODE,
    )


DEBUGGING = "debugpy" in sys.modules


def prepare_for_dev(debugging: bool = DEBUGGING) -> None:
    options.DEV_MODE = True

    # if we are not debugging, which requires RELOAD == False,
    # we set the RELOAD to True to simplify the development
    if not debugging:
        options.RELOAD = True


parser = argparse.ArgumentParser(
    prog="insurance_calculator_service"
)
parser.add_argument(
    "--host",
    default="localhost",
    help="change where app will be hosted, default is 'localhost'",
)
parser.add_argument(
    "--log-to-file",
    action="store_true",
    help="log into 'app.log' file instead of stdout",
)
parser.add_argument(
    "--dev-mode",
    action="store_true",
    help="log into 'app.log' file instead of stdout",
)


def main(argv=sys.argv):
    args = parser.parse_args(argv[1:])

    if args.log_to_file:
        options.LOG_TO_FILE = True

    if args.dev_mode:
        prepare_for_dev()

    run(host=args.host)
