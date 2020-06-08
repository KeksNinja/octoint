from PySide2 import QtCore
from PySide2.QtCore import QRegExp, Qt
from PySide2.QtGui import QRegExpValidator
from PySide2.QtWidgets import QDialog, QVBoxLayout, QGroupBox, QComboBox, QLabel, QPushButton, QLineEdit

from octoint import create_client
from octoint.main_utils import octoint_logger
from octoint.setup.setup_model import get_profile_names, create_info_text, write_ip_and_api, write_config
from octoint.main_config import load_config

setup_view_logger = octoint_logger(__name__)


class Setup(QDialog):
    Config_Generated = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.octopi_settings = OctoPiSettings()
        self.setWindowTitle('Setup')

        self.resize(600, 100)

        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.on_connect_pressed)

        self.print_profiles = PrintProfiles()
        self.confirm_button = QPushButton('Confirm')

        self.Error = None

        self.h_layout = QVBoxLayout()
        self.h_layout.addWidget(self.octopi_settings)
        self.h_layout.addWidget(self.connect_button)

        self.config_generated = False

        self.setLayout(self.h_layout)

    def closeEvent(self, event):
        if self.config_generated:
            self.Config_Generated.emit()
            event.accept()
        else:
            event.ignore()

    def on_connect_pressed(self):
        write_ip_and_api(self)
        success = create_client()
        if success:
            self.confirm_button.clicked.connect(self.on_confirm_pressed)
            self.h_layout.addWidget(self.print_profiles)
            self.h_layout.addWidget(self.confirm_button)
            self.print_profiles.on_connection()
        else:
            self.Error = QLabel('Input wrong try again!')
            self.h_layout.addWidget(self.Error)

    def on_confirm_pressed(self):
        write_config(self)
        load_config()
        self.config_generated = True
        self.close()


class OctoPiSettings(QGroupBox):
    def __init__(self, parent=None):
        super(OctoPiSettings, self).__init__(parent)

        self.setTitle("Input Octopi Information:")
        main_layout = QVBoxLayout()

        self.ip_address = QLineEdit()
        self.ip_address.setPlaceholderText('Please Input IP Address of the Octopi')

        self.api_key = QLineEdit()
        self.api_key.setPlaceholderText('Please Input API Key of your Account')

        main_layout.addWidget(self.ip_address)
        main_layout.addWidget(self.api_key)

        self.setLayout(main_layout)

        ip_reg = QRegExp("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)"
                         "{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        ip_reg.setCaseSensitivity(Qt.CaseInsensitive)
        ip_reg.setPatternSyntax(QRegExp.RegExp)

        regValidator = QRegExpValidator()
        regValidator.setRegExp(ip_reg)
        self.ip_address.setValidator(regValidator)


class PrintProfiles(QGroupBox):
    def __init__(self, parent=None):
        super(PrintProfiles, self).__init__(parent)

        self.setTitle("Select Printerprofile:")
        self.setFlat(True)
        self.setMinimumWidth(500)

        self.main_layout = QVBoxLayout()

        self.profiles_menu = QComboBox()
        self.profiles_menu.setVisible(False)
        self.main_layout.addWidget(self.profiles_menu)

        self.info_label = QLabel()
        self.info_label.setVisible(False)
        self.main_layout.addWidget(self.info_label)

        self.setLayout(self.main_layout)

    def on_connection(self):
        self.profiles_menu.addItems(get_profile_names())
        info_text = create_info_text(self.profiles_menu.currentText())
        self.info_label.setText(info_text)
        self.info_label.setVisible(True)
        self.profiles_menu.setVisible(True)


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)

    octoint_window = Setup()
    octoint_window.show()

    sys.exit(app.exec_())
