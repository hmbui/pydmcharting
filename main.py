from setup_paths import setup_paths
setup_paths()

import os
from arg_parser import ArgParser
from version import VERSION
import traceback

from pydmcharting_logging import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from displays.main_display import PyDMChartingDisplay


def main():
    _parse_arguments()

    pydm_chartsdipslay = PyDMChartingDisplay()
    pydm_chartsdipslay.show()


def _parse_arguments():
    """
    Parse the command arguments.

    Returns
    -------
    The command arguments as a dictionary : dict
    """
    parser = ArgParser(description="A charting tool.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--version", action="version", version=VERSION)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        logger.error("Unexpected exception during the charting process. Exception type: {0}. Exception: {1}"
                     .format(type(error), error))
