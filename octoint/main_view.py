import qdarkstyle
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QDockWidget, QStatusBar

from octoint.sensors import show as generate_sensors
from octoint.printsettings import show as generate_printsettings
from octoint.viewers import show as generate_viewers
from octoint.move import show as generate_move

from octoint.main_utils import octoint_logger
from octoint.main_config import CONFIG

main_view_logger = octoint_logger(__name__)


class OctoIntWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
        self.resize(2000, 1500)
        self.setWindowTitle(f'OctoInt for {CONFIG.print_model}')

        self.statusbar = None
        self.viewers = None
        self.printsettings = None

        self.main_layout = QVBoxLayout()
        self.create_status_bar()
        self.setup_main_layout()

    def setup_main_layout(self):
        self.viewers = generate_viewers()

        self.printsettings = generate_printsettings()

        self.printsettings.load_started.connect(self.on_select_started)
        self.printsettings.load_finished.connect(self.on_select_finished)

        printsettings_dock = QDockWidget("Printsettings", self)
        printsettings_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        printsettings_dock.setWidget(self.printsettings)
        self.addDockWidget(Qt.LeftDockWidgetArea, printsettings_dock)

        self.move_settings = generate_move()

        move_dock = QDockWidget("Move", self)
        move_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        move_dock.setWidget(self.move_settings)
        self.addDockWidget(Qt.LeftDockWidgetArea, move_dock)

        self.tabifyDockWidget(printsettings_dock, move_dock)
        printsettings_dock.raise_()

        sensor_dock = QDockWidget("Sensors", self)
        sensor_widget = generate_sensors()
        sensor_dock.setWidget(sensor_widget)
        sensor_dock.setAllowedAreas(Qt.LeftDockWidgetArea)

        self.addDockWidget(Qt.LeftDockWidgetArea, sensor_dock)
        self.setCentralWidget(self.viewers)

    def create_status_bar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage('Ready')

    def on_select_started(self):
        self.statusbar.clearMessage()
        self.statusbar.showMessage("Downloading Gcode")

    def on_select_finished(self):
        self.viewers.gl_widget.update_gcode()
        self.statusbar.clearMessage()
        self.statusbar.showMessage("Ready")