from PySide2.QtGui import QColor

from octoint.main_utils import octoint_logger, timer, Worker
from octoint.sensors.temp_utils import set_tool_target, set_bed_target, \
    get_temp_dict

temp_view_logger = octoint_logger(__name__)


temp_window = None
temp_worker = Worker()


def update_plot(temp_widget):
    """Start Worker Thread to update Chart"""

    global temp_worker

    temp_worker.setup(get_temp_dict, emit_dict=True, additional_data=temp_widget)
    temp_worker.dataSignal.connect(on_temp_data_sent)

    if temp_worker.isRunning():
        temp_worker.stop()
    else:
        temp_worker.start()


time_counter = 0
time_range = 300


@timer(temp_view_logger)
def plot(temp_widget, temp_data):
    """
    Update Chart Widget Data
    :param temp_widget:(octoint.sensors.temp_view.Temperature_Widget)  Chart to add data to
    :param temp_data: (list) data containing Target and Current Tool/Bed Temperature
    """

    global time_counter
    time_counter += 1

    bed_temperature, bed_target_temperature = temp_data[0]
    tool_temperature, tool_target_temperature = temp_data[1]

    min_target_temperature = min(bed_target_temperature, tool_target_temperature, bed_temperature, tool_temperature)
    max_target_temperature = max(bed_target_temperature, tool_target_temperature, bed_temperature, tool_temperature)

    temp_widget.Temp_Chart.bed_series.append(time_counter, bed_temperature)
    if temp_widget.Temp_Chart.bed_series.count() > time_range:
        temp_widget.Temp_Chart.bed_series.remove(0)

    temp_widget.Temp_Chart.tool_series.append(time_counter, tool_temperature)
    if temp_widget.Temp_Chart.tool_series.count() > time_range:
        temp_widget.Temp_Chart.tool_series.remove(0)

    temp_widget.Temp_Chart.chart().createDefaultAxes()

    temp_widget.Temp_Chart.chart().axisX().setRange(max(time_counter-time_range, 0), time_counter)
    temp_widget.Temp_Chart.chart().axisY().setRange(max(min_target_temperature - 50, 0), max_target_temperature + 10)

    temp_widget.Temp_Chart.chart().axisX().setLabelsColor(QColor(255, 255, 255, 255))
    temp_widget.Temp_Chart.chart().axisY().setLabelsColor(QColor(255, 255, 255, 255))


def on_temp_data_sent(data):
    temp_widget = data['additional_data']
    bed_temp, tool_temp = data['result']
    data = [bed_temp, tool_temp]
    plot(temp_widget, data)


def set_tool_temperature(widget):
    temp = int(widget.tool_target.text())
    set_tool_target(temp)


def set_bed_temperature(widget):
    temp = int(widget.bed_target.text())
    set_bed_target(temp)
