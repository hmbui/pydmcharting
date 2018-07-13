import os
from pydm import Display

from pydmcharting_logging import logging
logger = logging.getLogger(__name__)


class PyDMChartingDisplay(Display):
    PYDMCHARTING_UI_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "pydmcharting_graph.ui")

    def __init__(self, parent=None, args=[]):
        super(PyDMChartingDisplay, self).__init__(parent=parent, args=args)

    def ui_filename(self):
        return self.PYDMCHARTING_UI_FILENAME

    def ui_filepath(self):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())

