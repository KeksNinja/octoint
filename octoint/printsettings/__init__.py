from octoint import update_timer
from octoint.printsettings.printsettings_view import PrintSettings
from octoint.printsettings.printsettings_model import upload_file_pressed, select_file_pressed, delete_file_pressed, \
    print_file_pressed, pause_file_pressed, restart_file_pressed, cancel_file_pressed, update_selected_file, update_list, update

PrintSettings = PrintSettings()


def show() -> PrintSettings:
    """
    Function to generate and show PrintSettings Window
    :return:(octoint.printsettings.printsettings_view.PrintSettings) Instance of Print Settings Window
    """

    PrintSettings.File_Loader.upload_PB.clicked.connect(lambda: upload_file_pressed(PrintSettings))
    PrintSettings.File_Loader.select_PB.clicked.connect(lambda: select_file_pressed(PrintSettings))
    PrintSettings.File_Loader.delete_PB.clicked.connect(lambda: delete_file_pressed(PrintSettings))

    PrintSettings.Selected_Print.print_PB.clicked.connect(print_file_pressed)
    PrintSettings.Selected_Print.pause_PB.clicked.connect(lambda: pause_file_pressed(PrintSettings))
    PrintSettings.Selected_Print.restart_PB.clicked.connect(restart_file_pressed)
    PrintSettings.Selected_Print.cancel_PB.clicked.connect(cancel_file_pressed)

    PrintSettings.File_Loader.File_List.itemActivated.connect(lambda: select_file_pressed(PrintSettings))

    update_selected_file(PrintSettings)
    update_list(PrintSettings)

    update_timer.timeout.connect(lambda: update(PrintSettings))

    return PrintSettings
