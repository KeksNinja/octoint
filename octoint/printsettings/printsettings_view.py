from PySide2 import QtCore
from PySide2.QtWidgets import QListWidget, QVBoxLayout, QDialog, QGroupBox, QPushButton, \
    QHBoxLayout, QLabel, QProgressBar, QFrame

from octoint.printsettings.printsettings_utils import file_names, setup_button_icon


class PrintSettings(QDialog):
    """Widget containing all Print Settings including the Selected Print information and the File List"""

    load_started = QtCore.Signal()
    load_finished = QtCore.Signal()

    upload_started = QtCore.Signal()
    upload_finished = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.Selected_Print = SelectedPrint()
        self.File_Loader = FileLoader()

        h_layout = QVBoxLayout()
        h_layout.addWidget(self.Selected_Print)
        h_layout.addWidget(self.File_Loader)

        self.setLayout(h_layout)

    def on_load_started(self):
        self.load_started.emit()

    def on_loaded(self):
        self.load_finished.emit()


class SelectedPrint(QGroupBox):
    """Display Information of current selected print"""

    def __init__(self):
        super().__init__()
        self.setTitle("Selected Print")
        self.setFlat(True)
        self.setMinimumWidth(500)
        self.main_layout = QVBoxLayout()
        self.information()
        self.print_actions()
        self.setLayout(self.main_layout)

    def information(self):
        """create all printer information such as current state, selected file and current user"""

        self.state = QLabel("Current State: ")

        self.h_frame0 = QFrame()
        self.h_frame0.setFrameShape(QFrame.HLine)

        self.file_name = QLabel("File Name: ")
        self.uploaded = QLabel("Uploaded: ")
        self.user = QLabel("User: ")

        self.h_frame1 = QFrame()
        self.h_frame1.setFrameShape(QFrame.HLine)

        self.time_elapsed = QLabel("Time Elapsed: ")
        self.time_remaining = QLabel("Time Left: ")
        self.time_finished = QLabel("Time to Finish: ")

        self.h_frame2 = QFrame()
        self.h_frame2.setFrameShape(QFrame.HLine)

        self.print_percentage = QLabel("Progress: ")
        self.print_percentage_progress = QProgressBar()
        self.print_percentage_progress.setTextVisible(False)

        self.main_layout.addWidget(self.state)
        self.main_layout.addWidget(self.h_frame0)

        self.main_layout.addWidget(self.file_name)
        self.main_layout.addWidget(self.uploaded)
        self.main_layout.addWidget(self.user)
        self.main_layout.addWidget(self.h_frame1)

        self.main_layout.addWidget(self.time_elapsed)
        self.main_layout.addWidget(self.time_remaining)
        self.main_layout.addWidget(self.time_finished)
        self.main_layout.addWidget(self.h_frame2)
        self.main_layout.addWidget(self.print_percentage)
        self.main_layout.addWidget(self.print_percentage_progress)

    def print_actions(self):
        """create all print command buttons"""

        h_layout = QHBoxLayout()

        self.print_PB = QPushButton()
        setup_button_icon(self.print_PB, "./octoint/resources/icons/print.png")

        self.pause_PB = QPushButton()
        setup_button_icon(self.pause_PB, "./octoint/resources/icons/pause.png")

        self.restart_PB = QPushButton()
        setup_button_icon(self.restart_PB, "./octoint/resources/icons/restart.png")

        self.cancel_PB = QPushButton()
        setup_button_icon(self.cancel_PB, "./octoint/resources/icons/cancel.png")

        h_layout.addStretch()

        h_layout.addWidget(self.print_PB)
        h_layout.addWidget(self.pause_PB)
        h_layout.addWidget(self.restart_PB)
        h_layout.addWidget(self.cancel_PB)

        self.main_layout.addLayout(h_layout)


class FileLoader(QGroupBox):
    """Contains upload select and delete button for uploaded files with the file list widget"""

    def __init__(self):
        super().__init__()
        self.setTitle("File Options")
        self.setFlat(True)
        self.setMinimumWidth(500)

        self.main_layout = QVBoxLayout()
        self.File_List = FileList()
        self.main_layout.addWidget(self.File_List)
        self.buttons()
        self.setLayout(self.main_layout)

    def buttons(self):
        self.h_layout = QHBoxLayout()
        self.main_layout.addLayout(self.h_layout)

        self.upload_PB = QPushButton()
        setup_button_icon(self.upload_PB, "./octoint/resources/icons/upload.png")

        self.select_PB = QPushButton()
        setup_button_icon(self.select_PB, "./octoint/resources/icons/select.png")

        self.delete_PB = QPushButton()
        setup_button_icon(self.delete_PB, "./octoint/resources/icons/delete.png")

        self.h_layout.addStretch(1)

        self.h_layout.addWidget(self.upload_PB)
        self.h_layout.addWidget(self.select_PB)
        self.h_layout.addWidget(self.delete_PB)


class FileList(QListWidget):
    """Slightly modified QListWidget for populated list"""

    def __init__(self):
        super().__init__()
        self.file_dict = file_names()
        self.setAlternatingRowColors(True)
