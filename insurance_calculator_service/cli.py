"""
Command line interface for the application
"""

import argparse
import sys

from . import options, run


parser = argparse.ArgumentParser(
    prog="SBDY_app", description="Run web app that simulates an online shop"
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


def main(argv=sys.argv):
    args = parser.parse_args(argv[1:])

    if args.log_to_file:
        options.LOG_TO_FILE = True

    run.run(host=args.host)
