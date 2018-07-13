import os
import sys

from pydmcharting_logging import logging
logger = logging.getLogger(__name__)


def setup_paths():
    PYDM_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pydm")
    sys.path.insert(1, PYDM_PATH)



