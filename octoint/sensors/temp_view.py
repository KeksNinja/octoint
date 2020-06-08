from PySide2.QtGui import QColor, QPen, QFont, QBrush, Qt, QPainter, QIntValidator
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QColor, QPen, QFont
from PySide2.QtWidgets import QVBoxLayout, QWidget, QLineEdit, QHBoxLayout


class Chart_Widget(QtCharts.QChartView):
    """Chart Widget containing all Temperature Data"""

    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)
        self.chart().setTheme(QtCharts.QChart.ChartThemeQt)
        self.chart().setBackgroundVisible(False)
        self.chart().setFont(QFont("Calibri"))
        self.bed_series = QtCharts.QSplineSeries()
        self.bed_series.setName("Bed Temperature")
        self.bed_series.setPen(QPen(QColor("#d9990b"), 2.5))
        # TODO set series label font color!!

        self.chart().setTitleBrush(QBrush(Qt.white))
        self.chart().addSeries(self.bed_series)

        self.tool_series = QtCharts.QSplineSeries()
        self.tool_series.setName("Tool Temperature")
        self.tool_series.setPen(QPen(QColor("#a99b76"), 2.5))

        self.chart().addSeries(self.tool_series)

        self.chart().legend().setLabelColor(QColor(255,255,255,255))


class Temperature_Widget(QWidget):
    """Widget containing the Target Temperature Input Fields and the Temperature Chart"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setMinimumHeight(500)
        self.setMinimumWidth(700)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.Temp_Chart = Chart_Widget()
        self.main_layout.addWidget(self.Temp_Chart)

        self.target_values()

    def target_values(self):
        """Setup Target Temperature Fields"""

        h_layout = QHBoxLayout()

        self.tool_target = QLineEdit()
        self.bed_target = QLineEdit()

        self.tool_target.setValidator(QIntValidator(0, 250, self))
        self.bed_target.setValidator(QIntValidator(0, 100, self))

        self.tool_target.setMaximumWidth(200)
        self.bed_target.setMaximumWidth(200)

        self.tool_target.setPlaceholderText('Nozzle Target Temperature')
        self.bed_target.setPlaceholderText('Bed Target Temperature')

        h_layout.addStretch()
        h_layout.addWidget(self.tool_target)
        h_layout.addWidget(self.bed_target)

        self.main_layout.addLayout(h_layout)
