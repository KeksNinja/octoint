import sys

import qdarkstyle
from PySide2 import QtGui
from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QIcon, QPixmap, QIntValidator
from PySide2.QtWidgets import QDialog, QGridLayout, QApplication, QPushButton, QLabel, QVBoxLayout, QFrame, QSlider, \
        QLineEdit

from octoint.move.move_model import move_x, move_y, move_z, home, extrude, update_increment


class MoveWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())

        self.main_layout = QVBoxLayout()

        #########################################################
        # Move Layout
        self.move_layout = QGridLayout()

        self.move_xy = QLabel('X, Y:')
        self.move_xy.setMaximumWidth(50)

        self.move_z = QLabel('Z:')
        self.move_z.setMaximumWidth(50)

        self.up = QPushButton()
        self.up.clicked.connect(lambda: move_y(1))
        self.down = QPushButton()
        self.down.clicked.connect(lambda: move_y(-1))
        self.right = QPushButton()
        self.right.clicked.connect(lambda: move_x(1))
        self.left = QPushButton()
        self.left.clicked.connect(lambda: move_x(-1))

        self.home = QPushButton()
        self.home.clicked.connect(home)

        self.up_z = QPushButton()
        self.up_z.clicked.connect(lambda: move_z(1))
        self.down_z = QPushButton()
        self.down_z.clicked.connect(lambda: move_z(-1))

        # 00 01 02 03
        # 10 11 12 13
        # 20 21 22 23
        # 30 31 32 33

        self.move_layout.addWidget(self.move_xy, 0, 0)

        self.move_layout.addWidget(self.up,     1, 1)
        self.move_layout.addWidget(self.down,   3, 1)
        self.move_layout.addWidget(self.left,   2, 0)
        self.move_layout.addWidget(self.right,  2, 2)

        self.move_layout.addWidget(self.home, 2, 1)

        self.move_layout.addWidget(self.move_z, 0, 3)

        self.move_layout.addWidget(self.up_z,     1, 4)
        self.move_layout.addWidget(self.down_z,   3, 4)

        self.move_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.main_layout.addLayout(self.move_layout)
        self.move_frame = QFrame()
        self.move_frame.setFrameShape(QFrame.HLine)
        self.main_layout.addWidget(self.move_frame)

        #########################################################
        # Extrude Layout
        self.extrude = QLabel('Extrude | Retract')
        self.main_layout.addWidget(self.extrude)

        self.extrude_layout = QGridLayout()

        self.ex_up = QPushButton()
        self.ex_up.clicked.connect(lambda: extrude(1))
        self.ex_down = QPushButton()
        self.ex_down.clicked.connect(lambda: extrude(-1))
        self.ex_up.setMaximumSize(150, 150)
        self.ex_down.setMaximumSize(150, 150)

        self.extrude_layout.addWidget(self.ex_up, 1, 1)
        self.extrude_layout.addWidget(self.ex_down, 3, 1)

        self.main_layout.addLayout(self.extrude_layout)
        #########################################################
        # Increment
        self.inc_layout = QVBoxLayout()

        self.inc_label = QLabel('Set Increment to move by in mm')
        self.inc_slider = QSlider(Qt.Orientation.Horizontal)
        self.inc_slider.setValue(10)

        self.inc_text = QLineEdit()
        self.inc_text.setPlaceholderText('Movement increment in mm')
        self.inc_text.setText('10')
        self.inc_text.setValidator(QIntValidator(0, 100))

        self.inc_slider.valueChanged.connect(self.on_slider_value_changed)
        self.inc_text.textChanged.connect(self.on_text_value_changed)

        self.inc_layout.addWidget(self.inc_label)
        self.inc_layout.addWidget(self.inc_slider)
        self.inc_layout.addWidget(self.inc_text)

        self.main_layout.addLayout(self.inc_layout)

        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.setLayout(self.main_layout)

        self.setup_icons()

    def on_slider_value_changed(self, value):
        self.inc_text.setText(str(value))
        update_increment(value)

    def on_text_value_changed(self, text):
        try:
            value = int(text)
        except ValueError:
            value = 0

        self.inc_slider.setValue(value)
        update_increment(value)

    def setup_icons(self):
        self.setup_button_icon(self.up, "./octoint/resources/icons/arrow.png", rotation=0)
        self.setup_button_icon(self.down, "./octoint/resources/icons/arrow.png", rotation=180)
        self.setup_button_icon(self.left, "./octoint/resources/icons/arrow.png", rotation=-90)
        self.setup_button_icon(self.right, "./octoint/resources/icons/arrow.png", rotation=90)
        self.setup_button_icon(self.home, "./octoint/resources/icons/home.png")

        self.setup_button_icon(self.up_z, "./octoint/resources/icons/arrow.png", rotation=0)
        self.setup_button_icon(self.down_z, "./octoint/resources/icons/arrow.png", rotation=180)

        self.setup_button_icon(self.ex_up, "./octoint/resources/icons/arrow.png", rotation=0)
        self.setup_button_icon(self.ex_down, "./octoint/resources/icons/arrow.png", rotation=180)

    @classmethod
    def setup_button_icon(cls, button, icon, size=50, rotation=0):
        """
        Add Icon to button
        :param button: (PySide2.QtWidgets.QPushButton) Button to add Icon to
        :param icon: (str) path to Icon file
        :param size: (int) size of Icon
        :param rotation: (float) rotation of Icon
        """

        icon_map = QPixmap(icon)

        transform = QtGui.QTransform().rotate(rotation)
        icon_map = icon_map.transformed(transform, Qt.SmoothTransformation)

        upload_button_icon = QIcon(icon_map)
        button.setIcon(upload_button_icon)
        button.setIconSize(QSize(size, size))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    move_window = MoveWindow()
    move_window.show()
    sys.exit(app.exec_())


