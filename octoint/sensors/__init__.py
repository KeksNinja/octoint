from PySide2 import QtCore

from octoint import update_timer
from octoint.sensors.temp_view import Temperature_Widget
from octoint.sensors.temp_model import time_counter, temp_window, set_tool_temperature, set_bed_temperature, \
    update_plot
from octoint.sensors.temp_utils import set_bed_target, set_tool_target


def show() -> Temperature_Widget:
    """
    Function to generate and show OctoInt Window
    :return:(octoint.sensors.temp_view.Temperature_Widget) Instance of Temperature Sensor Window
    """

    Temp_Window = Temperature_Widget()
    Temp_Window.tool_target.returnPressed.connect(lambda: set_tool_temperature(Temp_Window))
    Temp_Window.bed_target.returnPressed.connect(lambda: set_bed_temperature(Temp_Window))

    update_timer.timeout.connect(lambda: update_plot(Temp_Window))
    return Temp_Window
