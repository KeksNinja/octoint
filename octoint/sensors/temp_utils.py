from octoint import client
from octoint.main_utils import octoint_logger

temp_utils_logger = octoint_logger(__name__)

def get_bed_temp_dict():
    """
    Request Bed Temperature Data from Octopi
    :return:(dict) Bed Temperature Sensor Dictionary
    """

    try:
        bed_dict = client.bed(history=True, limit=10)['bed']
        return bed_dict['actual'], bed_dict['target']
    except KeyError as e:
        temp_utils_logger.warning(e)
        return 0, 0


def get_tool_temp_dict():
    """
    Request Tool Temperature Data from Octopi
    :return:(dict) Tool Temperature Sensor Dictionary
    """

    try:
        tool_dict = client.tool(history=True, limit=10)['tool0']
        return tool_dict['actual'], tool_dict['target']
    except KeyError as e:
        temp_utils_logger.warning(e)
        return 0, 0


def get_temp_dict():
    return get_bed_temp_dict(), get_tool_temp_dict()


def set_tool_target(temperature_target):
    """Set Tool target Temperature"""

    client.tool_target(temperature_target)


def set_bed_target(temperature_target):
    """Set Bed target Temperature"""

    client.bed_target(temperature_target)
