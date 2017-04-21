"""
Runs within the system tray -

- Looks at a given folder and creates a nested context on right-click.
- Nested menu will show all folders/files within the parent directory.
- Selecting a folder opens a new nested menu for that folder.
- Selecting a file copies the file contents to the clipboard.
"""

import sys
import os
import pyperclip
from configparser import ConfigParser
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu


class Config(object):
    def __init__(self, widget):
        self.src_dir = ''
        self.systray_icon = ''
        self.widget = widget

    def read_config(self):
        """
            Read config.ini file to set src_dir and systray_icon
        """
        if os.path.isfile("config.ini"):
            config = ConfigParser()
            config.read("config.ini")
            self.src_dir = config.get('DEFAULTS', 'MultiClip_Directory')
            self.systray_icon = config.get('DEFAULTS', 'System_Tray_Icon')
            config_status = 1
        else:
            config_status = 0
        return config_status

    def write_config(self):
        """
            Write config.ini after prompting user for input via popup input box
        """
        self.src_dir = self.get_src_dir()
        self.systray_icon = self.get_systray_icon()

        with open("config.ini", "w") as file:
            text = "[DEFAULTS]\nMultiClip_Directory = {0}\nSystem_Tray_Icon = {1}\n"
            file.write(text.format(self.src_dir, self.systray_icon))

    def get_src_dir(self):
        """
            Input prompt popup for src_dir, sets value globally for import.
            Calls 'popup' if value entered is not a valid directory path
        """
        text, okPressed = QInputDialog.getText(widget, "Configuration",
                                               "MultiClip directory:",
                                               QLineEdit.Normal,
                                               "")
        if okPressed:
            if os.path.isdir(text):
                return text
            else:
                self.popup("Not a valid directory", text)
                self.get_src_dir()
        else:
            exit()

    def get_systray_icon(self):
        """
            Check directory for "multiclip.ico".
            If unable to find, ask user to navigate to ico file
        """
        if os.path.isfile("multiclip.ico"):
            return "multiclip.ico"
        else:
            text, okPressed = QInputDialog.getText(widget, "Configuration",
                                                   "MultiClip system tray icon :",
                                                   QLineEdit.Normal,
                                                   "")
            if okPressed:
                if os.path.isfile(text):
                    if text[-3:].lower() == "ico":
                        return text
                    else:
                        self.popup("File must be .ico format", text)
                        self.get_systray_icon()
                else:
                    self.popup("Not a valid filepath", text)
                    self.get_systray_icon()
            else:
                exit()

    def popup(self, error, path):
        """
            Create a warning popup box
        """
        buttonReply = QMessageBox.warning(widget, 'Config Error',
                                          "{0}: \n{1}".format(error, path),
                                          QMessageBox.Ok | QMessageBox.Close)
        if buttonReply == QMessageBox.Ok:
            return 0
        if buttonReply == QMessageBox.Close:
            exit()


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, src_dir, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        # QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)

        self.list_subfolders(src_dir, menu)
        self.setContextMenu(menu)
        menu.addSeparator()
        self.create_exit(menu)

    def create_exit(self, menu):
        """
            Creates exit option in menu.
        """
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(lambda: exit())

    def list_subfolders(self, path, menu):
        """
            Detects subfolders, calls file lister for main folder.
            Recursively calls itself for subfolders.
        """
        for object_name in os.listdir(path):
            object_path = path + '/' + object_name
            if os.path.isdir(object_path):
                subfolder_menu = menu.addMenu(object_name)
                self.list_subfolders(object_path, subfolder_menu)
        self.list_files(path, menu)

    def list_files(self, path, menu):
        """
            Lists txt files in the folder.
        """
        for file_name in os.listdir(path):
            file_path = path + '/' + file_name
            if os.path.isfile(file_path):
                if file_path[-3:] == "txt":
                    self.add_file_to_menu(file_name, file_path, menu)

    def add_file_to_menu(self, file_name, file_path, menu):
        """
            Create file in the menu.
        """
        file_menu = menu.addAction(file_name)
        file_menu.triggered.connect(lambda: self.copy_contents(file_path))

    def copy_contents(self, object_path):
        """
            Copies the selected files contents to clipboard.
        """
        with open(object_path, "r") as file:
            txt_to_copy = file.read()
        pyperclip.copy(txt_to_copy)


def main(image, src_dir, application, widget):
    tray_icon = SystemTrayIcon(QtGui.QIcon(image), src_dir, widget)
    tray_icon.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    application = QApplication(sys.argv)
    widget = QWidget()
    config = Config(widget)
    config_status = config.read_config()
    if config_status == 0:
        config.write_config()
        config.read_config()
    image = config.systray_icon
    src_dir = config.src_dir
    main(image, src_dir, application, widget)
