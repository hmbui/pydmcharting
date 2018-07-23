import os
from pydm import Display
from pydm.widgets.timeplot import PyDMTimePlot

from pydmcharting_logging import logging
logger = logging.getLogger(__name__)

from setup_paths import setup_paths
setup_paths()

from pydm.PyQt import uic
from pydm.PyQt.QtGui import QApplication, QWidget, QCheckBox, QBrush, QColor, QPalette, QVBoxLayout, QSplitter
from pydm.PyQt.QtCore import Qt, QObject, QEvent, pyqtSlot
from utilities.utils import random_color


class PyDMChartingDisplay(Display):
    PYDMCHARTING_UI_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui", "pydmcharting_graph.ui")

    def __init__(self, parent=None, args=[]):
        super(PyDMChartingDisplay, self).__init__(parent=parent, args=args)
        self.channel_map = dict()

        self.chart = PyDMTimePlot()

        self.curve_panel_layout = QVBoxLayout()
        self.curve_panel_layout.setAlignment(Qt.AlignTop)
        self.curve_checkbox_panel = QWidget()
        self.curve_checkbox_panel.setLayout(self.curve_panel_layout)
        self.curve_checkbox_panel.setMinimumSize(0, 800)

        self.splitter = QSplitter(parent)
        self.splitter.addWidget(self.chart)
        self.splitter.addWidget(self.curve_checkbox_panel)

        self.charting_layout = self.ui.charting_layout
        self.charting_layout.addWidget(self.splitter)

        self.ui.pv_connect_push_button.clicked.connect(self.add_curve)
        self.ui.pv_name.installEventFilter(self)

    def ui_filename(self):
        return self.PYDMCHARTING_UI_FILENAME

    def ui_filepath(self):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())

    def eventFilter(self, obj, event):
        if obj == self.ui.pv_name and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self.add_curve()
                return True
            else:
                return super(PyDMChartingDisplay, self).eventFilter(obj, event)
        else:
            return super(PyDMChartingDisplay, self).eventFilter(obj, event)

    @pyqtSlot()
    def add_curve(self):
        pv_name = self.ui.pv_name.text()
        if pv_name:
            if pv_name in self.channel_map:
                logger.error("'{0}' has already been plotted.".format(pv_name))
                return
            color = random_color()
            self.chart.addYChannel(y_channel=pv_name, color=color, name=pv_name, lineStyle=Qt.SolidLine,
                                   lineWidth=2, symbol=None)
            self.channel_map[pv_name] = True
            self.generate_pv_checkboxes(pv_name, color)

            pydm_app = QApplication.instance()
            pydm_app.establish_widget_connections(self)

    def generate_pv_checkboxes(self, pv_name, curve_color):
        checkbox = QCheckBox()

        palette = checkbox.palette()
        palette.setColor(QPalette.Active, QPalette.WindowText, curve_color)
        checkbox.setPalette(palette)

        checkbox.setText(pv_name)
        checkbox.setChecked(True)
        self.curve_panel_layout.addWidget(checkbox)
