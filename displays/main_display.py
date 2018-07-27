# The Main Display Window

from functools import partial
import json

from pydm import Display
from pydm.widgets.timeplot import PyDMTimePlot

from pydmcharting_logging import logging
logger = logging.getLogger(__name__)

from setup_paths import setup_paths
setup_paths()

from pydm.PyQt.QtGui import QApplication, QWidget, QLabel, QCheckBox, QBrush, QColor, QPalette, QHBoxLayout,\
    QVBoxLayout, QSplitter, QComboBox, QLineEdit, QPushButton, QTabWidget
from pydm.PyQt.QtCore import Qt, QObject, QEvent, pyqtSlot, QSize
from displays.curve_settings_display import CurveSettingsDisplay
from utilities.utils import random_color


class PyDMChartingDisplay(Display):
    def __init__(self, parent=None, args=[], macros=None):
        """
        Create all the widgets, including any child dialogs.

        Parameters
        ----------
        parent : QWidget
            The parent widget of the charting display
        args : list
            The command parameters
        macros : str
            Macros to modify the UI parameters at runtime
        """
        super(PyDMChartingDisplay, self).__init__(parent=parent, args=args, macros=macros)

        self.channel_map = dict()
        self.setWindowTitle("PyDM Charting Tool")

        self.main_layout = QVBoxLayout()
        self.body_layout = QVBoxLayout()

        self.pv_layout = QHBoxLayout()
        self.pv_name_line_edt = QLineEdit()
        self.pv_name_line_edt.installEventFilter(self)
        self.pv_protocol_cmb = QComboBox()
        self.pv_protocol_cmb.addItems(["ca://", "archive://"])

        self.pv_connect_push_btn = QPushButton("Connect")
        self.pv_connect_push_btn.clicked.connect(self.add_curve)

        self.tab_panel = QTabWidget()
        self.curve_settings_tab = QWidget()
        self.chart_settings_tab = QWidget()

        self.charting_layout = QHBoxLayout()
        self.chart = PyDMTimePlot()
        self.chart.setPlotTitle("Time Plot")
        self.splitter = QSplitter()

        self.curve_settings_layout = QVBoxLayout()
        self.curve_settings_layout.setAlignment(Qt.AlignTop)
        self.curve_settings_layout.setSpacing(5)

        self.chart_settings_layout = QVBoxLayout()
        self.chart_settings_layout.setAlignment(Qt.AlignTop)
        self.chart_settings_layout.setSpacing(5)

        self.curve_checkbox_panel = QWidget()

        self.app = QApplication.instance()
        self.setup_ui()

        self.curve_settings_disp = None

    def minimumSizeHint(self):
        """
        The minimum recommended size of the main window.
        """
        return QSize(1024, 768)

    def ui_filepath(self):
        """
        The path to the UI file created by Qt Designer, if applicable.
        """
        # No UI file is being used
        return None

    def setup_ui(self):
        """
        Initialize the widgets and layouts.
        """
        self.setLayout(self.main_layout)

        self.pv_layout.addWidget(self.pv_protocol_cmb)
        self.pv_layout.addWidget(self.pv_name_line_edt)
        self.pv_layout.addWidget(self.pv_connect_push_btn)

        self.curve_settings_tab.layout = self.curve_settings_layout
        self.curve_settings_tab.setLayout(self.curve_settings_tab.layout)

        self.chart_settings_tab.layout = self.chart_settings_layout
        self.chart_settings_tab.setLayout(self.chart_settings_tab.layout)

        self.tab_panel.addTab(self.curve_settings_tab, "Curves")
        self.tab_panel.addTab(self.chart_settings_tab, "Chart")
        self.tab_panel.hide()

        self.splitter.addWidget(self.chart)
        self.splitter.addWidget(self.tab_panel)
        self.charting_layout.addWidget(self.splitter)

        self.body_layout.addLayout(self.pv_layout)
        self.body_layout.addLayout(self.charting_layout)
        self.main_layout.addLayout(self.body_layout)

    def eventFilter(self, obj, event):
        """
        Handle key and mouse events for any applicable widget.

        Parameters
        ----------
        obj : QWidget
            The current widget that accepts the event
        event : QEvent
            The key or mouse event to handle

        Returns
        -------
            True if the event was handled successfully; False otherwise
        """
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
        """
        Add a new curve to the chart.
        """
        pv_name = self._get_full_pv_name(self.pv_name_line_edt.text())
        if pv_name in self.channel_map:
            logger.error("'{0}' has already been plotted.".format(pv_name))
            return
        elif pv_name:
            color = random_color()
            curve = self.chart.addYChannel(y_channel=pv_name, color=color, name=pv_name, lineStyle=Qt.SolidLine,
                                           lineWidth=2, symbol=None, symbolSize=None)
            self.channel_map[pv_name] = curve
            self.generate_pv_checkbox(pv_name, color)

            self.app.establish_widget_connections(self)

    def generate_pv_checkbox(self, pv_name, curve_color):
        """
        Generate a set of widgets to manage the appearance of a curve. The set of widgets includes:
            1. A checkbox which shows the curve on the chart if checked, and hide the curve if not checked
            2. Two buttons -- Modify... and Remove. Modify... will bring up the Curve Settings dialog. Remove will
               delete the curve from the chart
        This set of widgets will be hidden initially, until the first curve is plotted.

        Parameters
        ----------
        pv_name: str
            The name of the PV the current curve is being plotted for

        curve_color : QColor
            The color of the curve to paint for the checkbox label to help the user track the curve to the checkbox
        """
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
        modify_curve_btn.setMaximumWidth(100)
        modify_curve_btn.clicked.connect(partial(self.display_curve_settings_dialog, pv_name))

        remove_curve_btn = QPushButton("Remove")
        remove_curve_btn.setObjectName(pv_name)
        remove_curve_btn.setMaximumWidth(100)
        remove_curve_btn.clicked.connect(partial(self.remove_curve, pv_name))

        curve_btn_layout.addWidget(modify_curve_btn)
        curve_btn_layout.addWidget(remove_curve_btn)

        self.curve_settings_layout.addWidget(checkbox)
        self.curve_settings_layout.addLayout(curve_btn_layout)
        self.tab_panel.show()

    @pyqtSlot()
    def handle_curve_chkbox_toggled(self, checkbox):
        """
        Handle a checkbox's checked and unchecked events.

        If a checkbox is checked, find the curve from the channel map. If found, re-draw the curve with its previous
        appearance settings.

        If a checkbox is unchecked, remove the curve from the chart, but keep the cached data in the channel map.

        Parameters
        ----------
        checkbox : QCheckBox
            The current checkbox being toggled
        """
        pv_name = self._get_full_pv_name(checkbox.text())
        if checkbox.isChecked():
            curve = self.channel_map.get(pv_name, None)
            if curve:
                self.chart.addYChannel(y_channel=curve.address, color=curve.color, name=curve.address,
                                       lineStyle=curve.lineStyle, lineWidth=curve.lineWidth, symbol=curve.symbol,
                                       symbolSize=curve.symbolSize)
            self.app.establish_widget_connections(self)
        else:
            curve = self.chart.findCurve(pv_name)
            if curve:
                self.chart.removeYChannel(curve)

    @pyqtSlot()
    def display_curve_settings_dialog(self, pv_name):
        """
        Bring up the Curve Settings dialog to modify the appearance of a curve.

        Parameters
        ----------
        pv_name : str
            The name of the PV the curve is being plotted for

        """
        self.curve_settings_disp = CurveSettingsDisplay(self, pv_name)
        self.curve_settings_disp.show()

    @pyqtSlot()
    def remove_curve(self, pv_name):
        """
        Remove a curve from the chart permanently. This will also clear the channel map cache from retaining the
        removed curve's appearance settings.

        Parameters
        ----------
        pv_name : str
            The name of the PV the curve is being plotted for
        """
        curve = self.chart.findCurve(pv_name)
        if curve:
            self.chart.removeYChannel(curve)
            del self.channel_map[pv_name]

            widgets = self.findChildren((QCheckBox, QPushButton), pv_name)
            for w in widgets:
                w.deleteLater()

    def _get_full_pv_name(self, pv_name):
        """
        Append the protocol to the PV Name.

        Parameters
        ----------
        pv_name : str
            The name of the PV the curve is being plotted for
        """
        if pv_name and "://" not in pv_name:
            pv_name = ''.join([self.pv_protocol_cmb.currentText(), pv_name])
        return pv_name
