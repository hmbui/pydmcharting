from pydm import Display
from pydm.widgets.baseplot import BasePlotCurveItem

from pydm.PyQt.QtCore import QSize
from pydm.PyQt.QtGui import QFormLayout, QLabel, QComboBox, QLineEdit, QSpinBox

class CurveSettingsDisplay(Display):
    def __init__(self, chart, parent=None):
        super(CurveSettingsDisplay, self).__init__(parent=parent)
        self.main_layout = QFormLayout()
        self.chart = chart
        self.pv_name = None

        self.setup_ui()

    def minimumSizeHint(self):
        # This is the default recommended size
        # for this screen
        return QSize(1024, 768)

    def ui_filepath(self):
        # No UI file is being used
        return None

    # @property
    # def pv_name(self):
    #     return self.pv_name
    #
    # @pv_name.setter
    # def pv_name(self, value):
    #     if value != self.pv_name:
    #         self.pv_name = value

    def setup_ui(self):
        symbol_lbl = QLabel("Symbol")
        symbol_cmb = QComboBox()

        for k, _ in BasePlotCurveItem.symbols.items():
            symbol_cmb.addItem(k)
        symbol_cmb.setCurrentIndex(0)
        symbol_cmb.currentIndexChanged.connect(self.handle_symbol_index_changed)

        symbol_size_lbl = QLabel("Symbol Size")
        symbol_size_spin = QSpinBox()
        symbol_size_spin.setRange(1, 5)

        line_style_lbl = QLabel("Line Style")
        line_style_cmb = QComboBox()

        for k, _ in BasePlotCurveItem.lines.items():
            line_style_cmb.addItem(k)
        line_style_cmb.setCurrentIndex(0)

        line_width_lbl = QLabel("Line Width")
        line_width_spin = QSpinBox()
        line_width_spin.setRange(1, 5)

        self.main_layout.addRow(symbol_lbl, symbol_cmb)
        self.main_layout.addRow(symbol_size_lbl, symbol_size_spin)
        self.main_layout.addRow(line_style_lbl, line_style_cmb)
        self.main_layout.addRow(line_width_lbl, line_width_spin)

        self.setLayout(self.main_layout)

    def handle_symbol_index_changed(self, new_index):
        curve = self.find_curve(self.pv_name)
        if curve:
            channel = curve.channel
            self.chart.remove

    def find_curve(self, pv_name):
        curves = self.chart.getCurves()
        return curves.get(pv_name, None)