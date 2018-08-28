# The Dialog to Export Data from a Chart

from functools import partial

from pydm.PyQt.QtCore import Qt, QSize
from pydm.PyQt.QtGui import QFormLayout, QCheckBox, QFileDialog, QLabel, QLineEdit

from pydm import Display


class AxisSettingsDisplay(Display):
    def __init__(self, main_display, parent=None):
        super(AxisSettingsDisplay, self).__init__(parent=parent)
        self.main_layout = QFormLayout()
        self.main_display = main_display

        self.chart = self.main_display.chart
        self.app = self.main_display.app

        self.x_axis_lbl = QLabel(text="x-axis Label")
        self.x_axis_label_line_edt = QLineEdit()
        self.x_axis_label_line_edt.textChanged.connect(partial(self.handle_axis_label_change, "bottom"))

        self.x_axis_unit_lbl = QLabel(text="x-axis Unit")
        self.x_axis_unit_edt = QLineEdit()
        self.x_axis_unit_edt.textChanged.connect(partial(self.handle_axis_label_change, "bottom", is_unit=True))

        self.y_axis_lbl = QLabel(text="y-axis Label")
        self.y_axis_label_line_edt = QLineEdit()
        self.y_axis_label_line_edt.textChanged.connect(partial(self.handle_axis_label_change, "left"))

        self.y_axis_unit_lbl = QLabel(text="y-axis Unit")
        self.y_axis_unit_edt = QLineEdit()
        self.y_axis_unit_edt.textChanged.connect(partial(self.handle_axis_label_change, "left", is_unit=True))

        self.display_right_y_axis_chk = QCheckBox(text="Display the right y-axis")
        self.display_right_y_axis_chk.setChecked(False)
        self.display_right_y_axis_chk.clicked.connect(self.handle_right_y_axis_checkbox_changed)

        self.setWindowTitle("Axis Settings")
        self.setFixedSize(QSize(300, 200))
        self.setWindowModality(Qt.ApplicationModal)

        self.setup_ui()

    def ui_filepath(self):
        """
        The path to the UI file created by Qt Designer, if applicable.
        """
        # No UI file is being used
        return None

    def setup_ui(self):
        # Add widgets to the form layout
        self.main_layout.setSpacing(10)
        self.main_layout.addRow(self.x_axis_lbl, self.x_axis_label_line_edt)
        self.main_layout.addRow(self.x_axis_unit_lbl, self.x_axis_unit_edt)
        self.main_layout.addRow(self.y_axis_lbl, self.y_axis_label_line_edt)
        self.main_layout.addRow(self.y_axis_unit_lbl, self.y_axis_unit_edt)
        self.main_layout.addRow(self.display_right_y_axis_chk, None)

        self.setLayout(self.main_layout)

    def handle_right_y_axis_checkbox_changed(self, is_checked):
        if is_checked:
            self.chart.showAxis("right")

            self.right_y_axis_lbl = QLabel(text="y-axis Label")
            self.right_y_axis_label_line_edt = QLineEdit()
            self.right_y_axis_label_line_edt.textChanged.connect(partial(self.handle_axis_label_change, "right"))

            self.right_y_axis_unit_lbl = QLabel(text="y-axis Unit")
            self.right_y_axis_unit_edt = QLineEdit()
            self.right_y_axis_unit_edt.textChanged.connect(
                partial(self.handle_axis_label_change, "right", is_unit=True))

            self.right_y_axis_label_line_edt.setText(self.y_axis_label_line_edt.text())
            self.right_y_axis_unit_edt.setText(self.y_axis_unit_edt.text())

            self.main_layout.addRow(self.right_y_axis_lbl, self.right_y_axis_label_line_edt)
            self.main_layout.addRow(self.right_y_axis_unit_lbl, self.right_y_axis_unit_edt)
        else:
            self.chart.showAxis("right", show=False)

            for i in range(2):
                self.main_layout.removeRow(self.main_layout.rowCount() - 1)

        self.app.establish_widget_connections(self.main_display)

    def handle_axis_label_change(self, axis_position, new_label, is_unit=False):
        if is_unit:
            self.chart.setLabel(axis_position, units=new_label)
        else:
            self.chart.setLabel(axis_position, text=new_label)

    def closeEvent(self, event):
        self.handle_close_button_clicked()

    def handle_close_button_clicked(self):
        """
        Close the dialog when the Close button is clicked.
        """
        self.close()
