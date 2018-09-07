
from collections import OrderedDict
import json

from pydm import utilities
from version import VERSION


class SettingsExporter:
    def __init__(self, pydm_main_display, include_pvs, include_chart_settings):
        self.main_display = pydm_main_display
        self.include_pvs = include_pvs
        self.include_chart_settings = include_chart_settings

    def export_settings(self, filename):
        settings = OrderedDict()
        settings["__version__"] = VERSION
        settings["pvs"] = OrderedDict()
        settings["chart_settings"] = OrderedDict()

        if self.include_pvs:
            pv_list = list()
            for k, v in self.main_display.channel_map.items():
                curve_settings = OrderedDict()
                curve_settings["color"] = v.color_string
                curve_settings["y_channel"] = v.address
                curve_settings["line_style"] = v.lineStyle
                curve_settings["line_width"] = v.lineWidth
                curve_settings["symbol"] = v.symbol
                curve_settings["symbol_size"] = v.symbolSize
                pv_list.append((k, curve_settings))
            for item in pv_list:
                settings["pvs"][item[0]] = item[1]
        if self.include_chart_settings:
            chart_settings = OrderedDict()
            chart = self.main_display.chart

            chart_settings["title"] = chart.getPlotTitle()

            chart_settings["x_axis_title"] = chart.labels["bottom"]
            chart_settings["x_axis_unit"] = chart.units["bottom"]

            chart_settings["left_y_axis_title"] = chart.labels["left"]
            chart_settings["left_y_axis_unit"] = chart.units["left"]

            chart_settings["right_y_axis_title"] = chart.labels["right"]
            chart_settings["right_y_axis_unit"] = chart.units["right"]

            chart_settings["redraw_rate"] = chart.maxRedrawRate
            chart_settings["data_sampling_mode"] = self.main_display.data_sampling_mode
            chart_settings["update_interval_hz"] = 1 / chart.getUpdateInterval()
            chart_settings["limit_time_span"] = self.main_display.chart_limit_time_span_chk.isChecked()

            time_span_limit_hours = self.main_display.chart_limit_time_span_hours_line_edt.text()
            time_span_limit_minutes = self.main_display.chart_limit_time_span_minutes_line_edt.text()
            time_span_limit_seconds = self.main_display.chart_limit_time_span_seconds_line_edt.text()

            chart_settings["time_span_limit_hours"] = time_span_limit_hours if time_span_limit_hours else 0
            chart_settings["time_span_limit_minutes"] = time_span_limit_hours if time_span_limit_minutes else 0
            chart_settings["time_span_limit_seconds"] = time_span_limit_hours if time_span_limit_seconds else 0

            chart_settings["buffer_size"] = chart.getBufferSize()
            chart_settings["show_legend"] = chart.getShowLegend()
            chart_settings["background_color"] = str(utilities.colors.svg_color_from_hex(
                chart.getBackgroundColor().name(), hex_on_fail=True))
            chart_settings["axis_color"] = str(utilities.colors.svg_color_from_hex(
                chart.getAxisColor().name(), hex_on_fail=True))
            chart_settings["show_x_grid"] = chart.getShowXGrid()
            chart_settings["show_y_grid"] = chart.getShowYGrid()
            chart_settings["grid_alpha"] = self.main_display.gridAlpha
            settings["chart_settings"].update(chart_settings)

        with open(filename, 'w') as json_file:
            json.dump(settings, json_file, separators=(',', ':'), indent=4)

