# The Dialog to Export Data from a Chart

from qtpy.QtCore import Qt, QSize
from qtpy.QtWidgets import QVBoxLayout, QCheckBox, QFileDialog, QLabel, QComboBox, QPushButton, QColorDialog
from qtpy.QtGui import QColor

from pyqtgraph.exporters import CSVExporter, ImageExporter

from pydm import Display
from data_io.settings_exporter import SettingsExporter


class PyDMChartImageExporter(ImageExporter):
    """
    Override the buggy widthChanged and heightChanged settings from pyqtgraph
    """
    def __init__(self, item):
        super(PyDMChartImageExporter, self).__init__(item=item)

    def widthChanged(self):
        sr = self.getSourceRect()
        ar = float(sr.height()) / sr.width()
        self.params.param('height').setValue(int(self.params['width']) * ar, blockSignal=self.heightChanged)

    def heightChanged(self):
        sr = self.getSourceRect()
        ar = float(sr.width()) / sr.height()
        self.params.param('width').setValue(int(self.params['height']) * ar, blockSignal=self.widthChanged)


class ChartDataExportDisplay(Display):
    def __init__(self, main_display, parent=None):
        super(ChartDataExportDisplay, self).__init__(parent=parent)
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_display = main_display

        self.export_options_lbl = QLabel()
        self.export_options_lbl.setText("Export Options")
        self.export_options_cmb = QComboBox()
        self.export_options_cmb.addItems(("Curve Data", "Chart Settings", "Image File (PNG, TIF, JPG, ...)"))
        self.export_options_cmb.currentIndexChanged.connect(self.handle_export_options_index_changed)

        # Options for Chart Settings
        self.include_pv_chk = QCheckBox("Include currently plotted PVs")
        self.include_pv_chk.setChecked(True)

        self.include_chart_settings_chk = QCheckBox("Include current chart settings")
        self.include_chart_settings_chk.setChecked(True)

        # Options for Image File
        self.anti_alias_chk = QCheckBox("Anti-alias")
        self.anti_alias_chk.setChecked(True)

        self.export_image_background_color_lbl = QLabel("Curve Color ")
        self.export_image_background_btn = QPushButton()
        self.export_image_background_btn.setMaximumWidth(20)
        self.export_image_background_btn.setStyleSheet("background-color: black")
        self.export_image_background_btn.clicked.connect(self.handle_export_image_background_button_clicked)

        self.export_format_lbl = QLabel()
        self.export_format_lbl.setText("Export Format")
        self.file_format_cmb = QComboBox()
        self.file_format_cmb.addItems(("csv", "json", "Image formats (PNG, TIF, JPG, ...)"))
        self.file_format = "*.csv"
        self.exported_image_background_color = QColor(Qt.black)

        self.save_file_btn = QPushButton("Export...")
        self.save_file_btn.clicked.connect(self.handle_save_file_btn_clicked)

        self.setFixedSize(QSize(300, 200))
        self.setWindowTitle("Export Chart Settings")
        self.setWindowModality(Qt.ApplicationModal)
        self.setup_ui()

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
        self.main_layout.addWidget(self.include_chart_settings_chk)
        self.main_layout.addWidget(self.anti_alias_chk)
        self.main_layout.addWidget(self.export_image_background_btn)
        self.main_layout.addWidget(self.export_format_lbl)
        self.main_layout.addWidget(self.file_format_cmb)
        self.main_layout.addWidget(self.save_file_btn)
        self.setLayout(self.main_layout)

        self.export_options_cmb.currentIndexChanged.emit(0)

    def handle_export_options_index_changed(self, selected_index):
        self.include_pv_chk.setVisible(selected_index == 1)
        self.include_chart_settings_chk.setVisible(selected_index == 1)
        self.anti_alias_chk.setVisible(selected_index == 2)
        self.export_image_background_btn.setVisible(selected_index == 2)

        self.file_format_cmb.setCurrentIndex(selected_index)
        self.file_format = "*." + self.file_format_cmb.currentText()
        self.file_format_cmb.setEnabled(False)

    def handle_save_file_btn_clicked(self):
        if self.export_options_cmb.currentIndex() == 2:
            pass
        else:
            saved_file_info = QFileDialog.getSaveFileName(self, caption="Save File", filter=self.file_format)
            saved_file_name = saved_file_info[0]
            if saved_file_info[1][1:] not in saved_file_name:
                saved_file_name += saved_file_info[1][1:]

            if saved_file_name:
                if self.export_options_cmb.currentIndex() == 0:
                    data_exporter = CSVExporter(self.main_display.chart.plotItem)
                    data_exporter.export(saved_file_name)
                else:
                    settings_exporter = SettingsExporter(self.main_display, self.include_pv_chk.isChecked(),
                                                         self.include_chart_settings_chk.isChecked())
                    settings_exporter.export_settings(saved_file_name)

    def handle_export_image_background_button_clicked(self):
        self.exported_image_background_color = QColorDialog.getColor()
        self.export_image_background_btn.setStyleSheet("background-color: " +
                                                       self.exported_image_background_color.name())
