import datetime

from PySide2.QtWidgets import QFileDialog

from octoint.printsettings.printsettings_utils import file_names, get_job_dict, round_time, upload_file, select_file, \
    delete_file, start_print, pause_print, \
    restart_print, cancel_print, setup_button_icon
from octoint.main_utils import octoint_logger, Worker

printsettings_model_logger = octoint_logger(__name__)

select_file_worker = Worker()
upload_file_worker = Worker()


def update_list(settings):
    """Reload full File List"""
    file_name_dict = file_names()

    names = list(file_name_dict.keys())
    if settings.File_Loader.File_List.count() is not len(names):
        settings.File_Loader.File_List.clear()
        settings.File_Loader.File_List.addItems(names)


def update_selected_file(settings):
    """Update Selected File Information for all Widgets"""
    c_job_dict = get_job_dict()
    if c_job_dict:
        settings.Selected_Print.state.setText("Current State: {}".format(c_job_dict['state']))
        settings.Selected_Print.file_name.setText("File Name: {}".format(c_job_dict['job']['file']['name']))

        try:
            upload_time = datetime.datetime.fromtimestamp(c_job_dict['job']['file']['date'])
            settings.Selected_Print.uploaded.setText("Uploaded: {}".format(upload_time))
            settings.Selected_Print.uploaded.setVisible(True)
        except TypeError:
            settings.Selected_Print.uploaded.setVisible(False)

        settings.Selected_Print.user.setText("User: {}".format(c_job_dict['job']['user']))

        try:
            time_elapsed = datetime.timedelta(seconds=c_job_dict['progress']['printTime'])
            settings.Selected_Print.time_elapsed.setText("Time Elapsed: {}".format(str(time_elapsed)))
            settings.Selected_Print.time_elapsed.setVisible(True)
            settings.Selected_Print.h_frame1.setVisible(True)
        except TypeError:
            settings.Selected_Print.time_elapsed.setVisible(False)
            settings.Selected_Print.h_frame1.setVisible(False)

        try:
            time_left = datetime.timedelta(seconds=c_job_dict['progress']['printTimeLeft'])
            settings.Selected_Print.time_remaining.setText("Time Left: {}".format(time_left))

            time_finished = datetime.datetime.now() + time_left
            time_finished = round_time(dt=time_finished)
            settings.Selected_Print.time_finished.setText("Time to Finish: {}".format(time_finished))

            print_percentage = (c_job_dict['progress']['filepos'] / c_job_dict['job']['file']['size'])
            dec_percent = round((print_percentage * 100), 4)
            settings.Selected_Print.print_percentage.setText("Progress: {}".format(dec_percent))

            settings.Selected_Print.print_percentage_progress.setValue(dec_percent)

            settings.Selected_Print.time_remaining.setVisible(True)
            settings.Selected_Print.time_finished.setVisible(True)
            settings.Selected_Print.print_percentage.setVisible(True)
            settings.Selected_Print.print_percentage_progress.setVisible(True)
        except TypeError:
            settings.Selected_Print.time_remaining.setVisible(False)
            settings.Selected_Print.time_finished.setVisible(False)
            settings.Selected_Print.print_percentage.setVisible(False)
            settings.Selected_Print.print_percentage_progress.setVisible(False)


def update(settings):
    """Update all Printsettings Widgets"""

    update_list(settings)
    update_selected_file(settings)


def upload_file_pressed(settings):
    global upload_file_worker
    try:
        dialog = QFileDialog.getOpenFileName()[0]
        upload_file_worker.setup(upload_file, args=[dialog])
        upload_file_worker.finished.connect(lambda: update_list(settings))
        upload_file_worker.start()

    except TypeError as e:
        printsettings_model_logger.error(f"File Selection Canceled {e}")


def select_file_pressed(settings):
    global select_file_worker

    try:
        selected_list_item = settings.File_Loader.File_List.selectedItems()[0].text()
        select_file_worker.setup(select_file, args=[selected_list_item])

        select_file_worker.started.connect(settings.on_load_started)
        select_file_worker.finished.connect(settings.on_loaded)

        if select_file_worker.isRunning():
            select_file_worker.stop()
        else:
            select_file_worker.start()

    except IndexError as e:
        printsettings_model_logger.error(f'Nothing Selected {e}')


def delete_file_pressed(settings):
    try:
        selected_list_item = settings.File_Loader.File_List.selectedItems()[0].text()
        delete_file(selected_list_item)
    except IndexError as e:
        printsettings_model_logger.error(f'Nothing Selected {e}')


def print_file_pressed():
    try:
        start_print()
    except RuntimeError:
        printsettings_model_logger.error('Nothing Selected')


def pause_file_pressed(settings):
    state = get_job_dict()['state']
    if state == "Pausing" or state == "Paused":
        setup_button_icon(settings.Selected_Print.pause_PB, "./octoint/resources/icons/pause.png")
        pause_print("resume")
    else:
        setup_button_icon(settings.Selected_Print.pause_PB, "./octoint/resources/icons/play.png")
        pause_print("pause")


def restart_file_pressed():
    restart_print()


def cancel_file_pressed():
    cancel_print()
