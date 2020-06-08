import sys

from PySide2.QtWidgets import QApplication
from octoint import show as generate_octoint

app = QApplication(sys.argv)
octoint_window = generate_octoint()
sys.exit(app.exec_())
