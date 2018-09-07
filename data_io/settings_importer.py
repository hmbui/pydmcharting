import json

from pydm.PyQt.Qt import QColor
from displays import main_display


class SettingsImporter:
    def __init__(self, pydm_main_display):
        self.main_display = pydm_main_display

    def import_settings(self, filename):
        with open(filename, 'r') as json_file:
            settings = json.load(json_file)
            self._parse(settings)

    def _parse(self, settings):
        pv_settings = settings["pvs"]

        for k, v in pv_settings.items():
            self.main_display.add_y_channel(pv_name=v["y_channel"], curve_name=k, color=QColor(v["color"]),
                                            line_style=v["line_style"], line_width=v["line_width"],
                                            symbol=v["symbol"], symbol_size=v["symbol_size"])
        chart_settings = settings["chart_settings"]
        if len(chart_settings):
            chart = self.main_display.chart

            self.main_display.chart_title_line_edt.textChanged.emit(chart_settings["title"])

            chart.setLabel("bottom", text=chart_settings["x_axis_title"])
            chart.setLabel("bottom", unit=chart_settings["x_axis_unit"])

            chart.setLabel("left", text=chart_settings["left_y_axis_title"])
            chart.setLabel("left", unit=chart_settings["left_y_axis_unit"])

            chart.setLabel("right", text=chart_settings["right_y_axis_title"])
            chart.setLabel("right", unit=chart_settings["right_y_axis_unit"])

            self.main_display.chart_redraw_rate_spin.valueChanged.emit(chart_settings["redraw_rate"])

            data_sampling_mode = chart_settings["data_sampling_mode"]
            self.main_display.chart_sync_mode_sync_radio.setChecked(data_sampling_mode == main_display.SYNC_DATA_SAMPLING)
            self.main_display.chart_sync_mode_async_radio.setChecked(data_sampling_mode == main_display.ASYNC_DATA_SAMPLING)
            self.main_display.chart_sync_mode_async_radio.toggled.emit(data_sampling_mode ==
                                                                       main_display.ASYNC_DATA_SAMPLING)

            self.main_display.chart_data_async_sampling_rate_spin.valueChanged.emit(chart_settings["update_interval_hz"])

            time_span_limit_hours = chart_settings["time_span_limit_hours"]
            self.main_display.chart_limit_time_span_hours_line_edt.setText(str(time_span_limit_hours))
            self.main_display.chart_limit_time_span_hours_line_edt.textChanged.emit(str(time_span_limit_hours))

            time_span_limit_minutes = chart_settings["time_span_limit_minutes"]
            self.main_display.chart_limit_time_span_minutes_line_edt.setText(str(time_span_limit_minutes))
            self.main_display.chart_limit_time_span_minutes_line_edt.textChanged.emit(str(time_span_limit_minutes))

            time_span_limit_seconds = chart_settings["time_span_limit_seconds"]
            self.main_display.chart_limit_time_span_seconds_line_edt.setText(str(time_span_limit_seconds))
            self.main_display.chart_limit_time_span_seconds_line_edt.textChanged.emit(str(time_span_limit_seconds))

            set_time_span = True
            if time_span_limit_hours == 0 and time_span_limit_minutes == 0 and time_span_limit_seconds == 0:
                set_time_span = False

            self.main_display.chart_limit_time_span_chk.setChecked(chart_settings["limit_time_span"] and set_time_span)
            self.main_display.chart_limit_time_span_chk.clicked.emit(chart_settings["limit_time_span"] and
                                                                     set_time_span)

            if set_time_span:
                self.main_display.chart_limit_time_span_activate_btn.clicked.emit()

            self.main_display.chart_ring_buffer_size_edt.textChanged.emit(str(chart_settings["buffer_size"]))

            self.main_display.show_legend_chk.setChecked(chart_settings["show_legend"])
            self.main_display.show_legend_chk.clicked.emit(chart_settings["show_legend"])

            background_color = QColor(chart_settings["background_color"])
            self.main_display.chart.setBackgroundColor(background_color)
            self.main_display.background_color_btn.setStyleSheet("background-color: " + background_color.name())

            axis_color = QColor(chart_settings["axis_color"])
            self.main_display.chart.setAxisColor(axis_color)
            self.main_display.axis_color_btn.setStyleSheet("background-color: " + axis_color.name())

            self.main_display.show_x_grid_chk.setChecked(chart_settings["show_x_grid"])
            self.main_display.show_x_grid_chk.clicked.emit(chart_settings["show_x_grid"])

            self.main_display.show_y_grid_chk.setChecked(chart_settings["show_y_grid"])
            self.main_display.show_y_grid_chk.clicked.emit(chart_settings["show_y_grid"])

            self.main_display.grid_opacity_slr.valueChanged.emit(chart_settings["grid_alpha"] )
