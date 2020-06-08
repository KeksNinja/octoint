from PySide2 import QtCore
from octoint.main_config import load_config

from octoint.rest_api import make_client

from octoint.main_utils import octoint_logger

octoint_logger_L = octoint_logger(__name__)

# Init Timer
update_timer = QtCore.QTimer()

client = None
octoint_window = None


def create_client():
    global client
    try:
        client = make_client()
        octoint_logger_L.debug('Connection Successful')
        return True
    except TypeError:
        return False


def show():
    """
    Function to generate either OctoInt Window or Setup Window if config.yaml does not exist
    :return:(octoint.main_view.OctoIntWindow) Instance of octoint Window
    """

    from octoint.setup import show as generate_setup

    setup_window = generate_setup()
    if setup_window:
        setup_window.Config_Generated.connect(generate_octoint_window)
        return setup_window
    else:
        load_config()
        return generate_octoint_window()


def generate_octoint_window():
    """
    Function to generate and show OctoInt Window
    :return:(octoint.main_view.OctoIntWindow) Instance of octoint Window
    """

    global client
    global octoint_window

    client = make_client()
    current_state = client.connection_info()['current']['state']
    if current_state == 'Closed' or 'Error' in current_state:
        client.connect()

    update_timer.start(3000)
    from octoint.main_view import OctoIntWindow

    octoint_window = OctoIntWindow()
    octoint_window.show()
    return octoint_window
