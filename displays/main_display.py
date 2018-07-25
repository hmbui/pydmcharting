from functools import partial
import json

from pydm import Display
from pydm.widgets.timeplot import PyDMTimePlot

from pydmcharting_logging import logging
logger = logging.getLogger(__name__)

from setup_paths import setup_paths
setup_paths()

from pydm.PyQt.QtGui import QApplication, QWidget, QLabel, QCheckBox, QBrush, QColor, QPalette, QHBoxLayout,\
    QVBoxLayout, QSplitter, QComboBox, QLineEdit, QPushButton
from pydm.PyQt.QtCore import Qt, QObject, QEvent, pyqtSlot, QSize
from displays.curve_settings_display import CurveSettingsDisplay
from utilities.utils import random_color


class PyDMChartingDisplay(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(PyDMChartingDisplay, self).__init__(parent=parent, args=args, macros=macros)

        self.channel_map = dict()

        self.main_layout = QVBoxLayout()
        self.title = QLabel("Charting Tool")

        self.body_layout = QVBoxLayout()

        self.pv_layout = QHBoxLayout()
        self.pv_name_line_edt = QLineEdit()
        self.pv_name_line_edt.installEventFilter(self)
        self.pv_protocol_cmb = QComboBox()
        self.pv_protocol_cmb.addItems(["ca://", "archive://"])

        self.pv_connect_push_btn = QPushButton("Connect")
        self.pv_connect_push_btn.clicked.connect(self.add_curve)

        self.charting_layout = QHBoxLayout()
        self.chart = PyDMTimePlot()
        self.splitter = QSplitter()

        self.curve_settings_layout = QVBoxLayout()
        self.curve_settings_layout.setSpacing(5)

        self.curve_panel_layout = QVBoxLayout()
        self.curve_panel_layout.addLayout(self.curve_settings_layout)

        self.curve_checkbox_panel = QWidget()

        self.app = QApplication.instance()
        self.setup_ui()

        self.curve_settings_disp = CurveSettingsDisplay(self.chart)

    def minimumSizeHint(self):
        # This is the default recommended size
        # for this screen
        return QSize(1024, 768)

    def ui_filepath(self):
        # No UI file is being used
        return None

    def setup_ui(self):
        self.setLayout(self.main_layout)

        self.title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title)

        self.pv_layout.addWidget(self.pv_protocol_cmb)
        self.pv_layout.addWidget(self.pv_name_line_edt)
        self.pv_layout.addWidget(self.pv_connect_push_btn)

        self.curve_panel_layout.setAlignment(Qt.AlignTop)
        self.curve_checkbox_panel.setLayout(self.curve_panel_layout)
        self.curve_checkbox_panel.setMinimumSize(0, 1000)

        self.splitter.addWidget(self.chart)
        self.splitter.addWidget(self.curve_checkbox_panel)
        self.charting_layout.addWidget(self.splitter)

        self.body_layout.addLayout(self.pv_layout)
        self.body_layout.addLayout(self.charting_layout)
        self.main_layout.addLayout(self.body_layout)

    def eventFilter(self, obj, event):
        if obj == self.pv_name_line_edt and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self.add_curve()
                return True
            else:
                return super(PyDMChartingDisplay, self).eventFilter(obj, event)
        else:
            return super(PyDMChartingDisplay, self).eventFilter(obj, event)

    @pyqtSlot()
    def add_curve(self):
        pv_name = self._get_full_pv_name(self.pv_name_line_edt.text())
        if pv_name in self.channel_map:
                logger.error("'{0}' has already been plotted.".format(pv_name))
                return
        elif pv_name:
            color = random_color()
            curve = self.chart.addYChannel(y_channel=pv_name, color=color, name=pv_name, lineStyle=Qt.SolidLine,
                                           lineWidth=2, symbol=None)
            self.channel_map[pv_name] = curve
            self.generate_pv_checkbox(pv_name, color)

            self.app.establish_widget_connections(self)

    def generate_pv_checkbox(self, pv_name, curve_color):
        checkbox = QCheckBox()
        checkbox.setObjectName(pv_name)

        palette = checkbox.palette()
        palette.setColor(QPalette.Active, QPalette.WindowText, curve_color)

        checkbox.setPalette(palette)
        checkbox.setText(pv_name.split("://")[1])
        checkbox.setChecked(True)
        checkbox.clicked.connect(partial(self.handle_curve_chkbox_toggled, checkbox))

        curve_btn_layout = QHBoxLayout()

        modify_curve_btn = QPushButton("Modify...")
        modify_curve_btn.setObjectName(pv_name)
        modify_curve_btn.clicked.connect(partial(self.display_curve_settings_dialog, pv_name))

        remove_curve_btn = QPushButton("Remove")
        remove_curve_btn.setObjectName(pv_name)
        remove_curve_btn.clicked.connect(partial(self.remove_curve, pv_name))

        curve_btn_layout.addWidget(modify_curve_btn)
        curve_btn_layout.addWidget(remove_curve_btn)

        self.curve_settings_layout.addWidget(checkbox)
        self.curve_settings_layout.addLayout(curve_btn_layout)

    @pyqtSlot()
    def handle_curve_chkbox_toggled(self, checkbox):
        pv_name = self._get_full_pv_name(checkbox.text())
        if checkbox.isChecked():
            curve = self.channel_map.get(pv_name, None)
            if curve:
                self.chart.addYChannel(y_channel=curve.address, color=curve.color, name=curve.address,
                                       lineStyle=curve.lineStyle, lineWidth=curve.lineWidth, symbol=curve.symbol)
            self.app.establish_widget_connections(self)
        else:
            curve = self.chart.findCurve(pv_name)
            if curve:
                self.chart.removeYChannel(curve)

    @pyqtSlot()
    def display_curve_settings_dialog(self, pv_name):
        self.curve_settings_disp.show()

    @pyqtSlot()
    def remove_curve(self, pv_name):
        curve = self.chart.findCurve(pv_name)
        if curve:
            self.chart.removeYChannel(curve)
            del self.channel_map[pv_name]

            widgets = self.findChildren((QCheckBox, QPushButton), pv_name)
            for w in widgets:
                w.deleteLater()

    def _get_full_pv_name(self, pv_name):
        if pv_name and "://" not in pv_name:
            pv_name = ''.join([self.pv_protocol_cmb.currentText(), pv_name])
        return pv_name


