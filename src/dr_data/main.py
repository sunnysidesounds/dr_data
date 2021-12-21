import os
import argparse
import logging
import sys
from dr_data.config import *

from dr_data import __version__

__author__ = "Jason R Alexander"
__copyright__ = "Jason R Alexander"
__license__ = "MIT"

_logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser(description="Utility tool that populates random or CSV data to your database for development purposes",
                                 epilog="Version: {version}".format(version=__version__))

def parse_args(args):
    parser.add_argument('-t', '--transplant', help="Insert one or all CSV files to table", action='store_true')
    parser.add_argument('-source', help="Used in conjuctions with `transplant` The CSV source file or directory", type=str)
    parser.add_argument('-destination', help="Used in conjuctions with `transplant` and `source`. if `source` is a file. destination table is required", type=str)

    parser.add_argument('-i', '--inject', help="Inserts one or many randomly regenerated rows", action='store_true')
    parser.add_argument('-rows', help="How may rows do you want to load per table in the database, default is set in configuration", type=int)

    parser.add_argument('-b', '--biopsy', help="Explicitly exports a table insertion-order JSON file", action='store_true')
    parser.add_argument('-export', help="The directory path to export the JSON file to, default is set in configuration ", type=str)

    parser.add_argument('-c', '--cleanse', help="Truncates all the values in the database", action='store_true')
    parser.add_argument('-config', help="configuration file or set {env_name}=<path> env variable".format(env_name=ENV_CONFIG_NAME), type=str)
    return parser.parse_args(args)

def setup_logging():
    log_format = "[%(asctime)s] %(levelname)s:%(name)s: %(message)s"
    logging.basicConfig(
        level=logging.INFO, stream=sys.stdout, format=log_format, datefmt="%Y-%m-%d %H:%M:%S"
    )

def main(args):
    print("--------------------------------------------------------------------------------------------------------")
    args = parse_args(args)
    configuration = os.getenv(ENV_CONFIG_NAME)
    if not args.config and not configuration:
        print("Error: please provide a configuration file. -config flag or set {env_name}=<path> env variable".format(env_name=ENV_CONFIG_NAME))
        sys.exit()
    if args.config:
        configuration = args.config

    setup_logging()

    if args.transplant:
        print("TODO transplant!")

    print("--------------------------------------------------------------------------------------------------------")


def run():
    main(sys.argv[1:])


if __name__ == '__main__':
    run()