import os

from octoint.setup.setup_model import update_info_text
from octoint.setup.setup_utils import config_path
from octoint.setup.setup_view import Setup


def show():
    """
    Function to generate and show OctoInt Window
    :return:(octoint.sensors.temp_view.Temperature_Widget) Instance of Temperature Sensor Window
    """

    if not os.path.exists(config_path):
        setup_window = Setup()
        setup_window.print_profiles.profiles_menu.currentTextChanged.connect(lambda: update_info_text(setup_window))
        setup_window.show()
        return setup_window
    else:
        return None


if __name__ == '__main__':
    import sys
    from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)
    octoint_window = show()
    octoint_window.show()
    sys.exit(app.exec_())
