from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon, QPixmap

from octoint import client

increment = 10


def update_increment(update):
    global increment
    increment = update


def move(x=None, y=None, z=None):
    client.jog(x=x, y=y, z=z)


def move_x(sign):
    move(x=increment*sign)


def move_y(sign):
    move(y=increment*sign)


def move_z(sign):
    move(z=increment*sign)


def home():
    client.home()


def extrude(sign):
    client.extrude(increment*sign)