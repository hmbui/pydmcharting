# The Dialog to Export Data from a Chart

from pydm.PyQt.QtCore import Qt
from pydm.PyQt.QtGui import QVBoxLayout, QCheckBox, QFileDialog, QLayout, QFormLayout, QLabel, QComboBox, QSpinBox, QPushButton, QColorDialog

from pydm import Display


class ChartDataExportDisplay(Display):
    def __init__(self, main_display, parent=None):
        super(ChartDataExportDisplay, self).__init__(parent=parent)
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(10)
        self.main_display = main_display

        self.export_options_lbl = QLabel()
        self.export_options_lbl.setText("Export Options")
        self.export_options_cmb = QComboBox()
        self.export_options_cmb.addItems(("Curve Data", "Chart Settings"))

        self.include_pv_chk = QCheckBox()
        self.include_pv_chk.setText("Include currently plotted PVs")
        self.include_pv_chk.setChecked(True)

        self.include_chart_settings = QCheckBox()
        self.include_chart_settings.setText("Include current chart settings")
        self.include_chart_settings.setChecked(True)

        self.export_format_lbl = QLabel()
        self.export_format_lbl.setText("Export Format")
        self.file_format_cmb = QComboBox()
        self.file_format_cmb.addItems(("csv", "json"))
        self.file_format = "*.csv"

        self.save_file_btn = QPushButton("Export...")
        self.save_file_btn.clicked.connect(self.handle_save_file_btn_clicked)

        self.setWindowTitle("Export Chart Settings")
        self.setWindowModality(Qt.ApplicationModal)
        self.setup_ui()
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def ui_filepath(self):
        """
        The path to the UI file created by Qt Designer, if applicable.
        """
        # No UI file is being used
        return None

    def setup_ui(self):
        self.main_layout.addWidget(self.export_options_lbl)
        self.main_layout.addWidget(self.export_options_cmb)
        self.main_layout.addWidget(self.include_pv_chk)
        self.main_layout.addWidget(self.include_chart_settings)
        self.main_layout.addWidget(self.export_format_lbl)
        self.main_layout.addWidget(self.file_format_cmb)
        self.main_layout.addWidget(self.save_file_btn)

        self.setLayout(self.main_layout)

    def handle_save_file_btn_clicked(self):
        saved_file_name = QFileDialog.getSaveFileName(self, caption="Save File", filter=self.file_format)
        print("Saved file name: {}".format(saved_file_name))
