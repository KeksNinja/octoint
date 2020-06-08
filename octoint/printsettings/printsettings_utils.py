import requests
import datetime

from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon, QPixmap

from octoint import client
from octoint.main_utils import octoint_logger
from octoint.main_config import CONFIG

printsettings_utils_logger = octoint_logger(__name__)

headers = {"Content-Type": "application/gcode",
           "X-Api-Key": CONFIG.api_key}

gcode_file_path = "./selected_file.gcode"


def setup_button_icon(button, icon, size=50):
    """
    Add Icon to button
    :param button: (PySide2.QtWidgets.QPushButton) Button to add Icon to
    :param icon: (str) path to Icon file
    :param size: (int) size of Icon
    """

    upload_button_icon = QIcon(QPixmap(icon))
    button.setIcon(upload_button_icon)
    button.setIconSize(QSize(size, size))


def file_names():
    """
    Get list of all files on octopi
    :return: (list) All Files stored on the octopi
    """
    file_dicts = client.files()['files']
    file_names_dict = {}
    for file_dict in file_dicts:
        file_names_dict[file_dict['name']] = file_dict['path']
    return file_names_dict


def get_job_dict():
    """
    :return: (dict) all infos about the current print job
    """
    return client.job_info()


def upload_file(file_path):
    """upload gcode file to octopi"""
    try:
        client.upload(file_path, location='local', select=True)
    except TypeError:
        printsettings_utils_logger.warning('upload aborted')


def select_file(file_path):
    """select file from list and overwrite current gcode file for preview"""
    client.select(file_path)

    job_dict = get_job_dict()
    file_origin = job_dict['job']['file']['origin']
    file_name = job_dict['job']['file']['name']
    file_url = client.files_info(file_origin, file_name)['refs']['download']
    r = requests.get(file_url, headers=headers)

    job_file = r.content
    with open(gcode_file_path, "wb") as f:
        f.write(job_file)


def delete_file(file_path):
    client.delete(file_path)


def start_print():
    client.start()


def pause_print(action):
    try:
        client.pause_command(action)
    except RuntimeError as e:
        printsettings_utils_logger.warning(f'Not Printing: {e}')


def restart_print():
    try:
        client.restart()
    except RuntimeError as e:
        printsettings_utils_logger.warning(f'Not Printing: {e}')


def cancel_print():
    try:
        client.cancel()
        client.home()
    except RuntimeError as e:
        printsettings_utils_logger.warning(f'Not Printing: {e}')


def round_time(dt=None, roundTo=1):
   """Round a datetime object to any time lapse in seconds
   dt : datetime.datetime object, default now.
   roundTo : Closest number of seconds to round to, default 1 minute.
   Author: Thierry Husson 2012 - Use it as you want but don't blame me.
   """
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)
