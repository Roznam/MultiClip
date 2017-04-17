'''
Multiclip -
- On initial launch prompts for the parent directory for MultiClip, writes a config file to store this information
- Creates a system tray icon, on right click displays a nested context menu displaying all subfolders and txt files
- Selecting a file copies the contents of the txt file to the clipboard

- Some functions have been removed and/or tweaked for compatibility with PyInstaller / Python 3.5.
'''

import sys
import os
import pyperclip
from configparser import ConfigParser
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QMessageBox


class Config(QWidget):
    def __init__(self):
        super().__init__()

        if self.read_config() == 1:
            self.read_config()
        else:
            self.write_config()
            self.read_config()

    def get_mc_dir(self):
        '''
            Input prompt popup for mc_dir, sets value globally for import
            Calls 'popup' if value entered is not a valid directory path
        '''
        global mc_dir
        text, okPressed = QInputDialog.getText(self, "Configuration", "MultiClip directory:", QLineEdit.Normal, "")
        if okPressed and os.path.isdir(text) is True:
            if text[-1] != "\\":
                mc_dir = text
            else:
                mc_dir = text
        else:
            self.popup("get_mc_dir", "Not a valid directory", text)

    def resource_path(self, relative_path):
        '''
            Get absolute path to resource, works for dev and for PyInstaller
        '''
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def get_systray_icon(self):
        '''
            Set systray variable to icon included with PyInstaller
        '''
        global systray_icon
        path_test = self.resource_path("multiclip.ico")
        systray_icon = path_test

    def popup(self, function, error, path):
        '''
            Create a warning popup box containing: Error, function that called for the popup and invalid path
        '''
        buttonReply = QMessageBox.warning(self, "Config Error",
                                          ("%s: \n" % error) + ("%s" % path), QMessageBox.Ok | QMessageBox.Close)
        if buttonReply == QMessageBox.Ok:
            if function == "get_mc_dir":
                self.get_mc_dir()
        if buttonReply == QMessageBox.Close:
            exit()

    def write_config(self):
        '''
            Writes config.ini after prompting user for input via popup input box
        '''
        self.get_mc_dir()

        with open("config.ini", "w") as file:
            file.write("[DEFAULTS]\n" +
                       ("MultiClip_Directory = %s\n" % mc_dir)
                       )

    def read_config(self):
        '''
            Reads config.ini file to set mc_dir and systray_icon
            Calls get_systray_icon
        '''
        config_status = None
        if os.path.isfile("config.ini"):
            try:
                global mc_dir
                self.get_systray_icon()
                config = ConfigParser()
                config.read("config.ini")
                mc_dir = config.get("DEFAULTS", "MultiClip_Directory")
                config_status = 1
            except:
                config_status = 0
        else:
            config_status = 0
        return config_status


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)

        self.list_subfolders(mc_dir, menu)
        self.setContextMenu(menu)
        menu.addSeparator()
        self.create_exit(menu)

    def create_exit(self, menu):
        '''
            Creates exit option in menu.
        '''
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.close)

    def close(self):
        '''
            Call to exit the program
        '''
        sys.exit(0)

    def list_subfolders(self, path, menu):
        '''
            Detects subfolders, calls file lister for main folder.
            Recursively calls itself for subfolders.
        '''
        for object_name in os.listdir(path):
            object_path = path + "/" + object_name
            if os.path.isdir(object_path) is True:
                subfolder_menu = self.create_submenu(object_name, menu)
                self.list_subfolders(object_path, subfolder_menu)
        self.list_files(path, menu)

    def create_submenu(self, subfolder_name, menu):
        '''
            Create submenu in the menu for subfolder.
        '''
        subfolder_menu = menu.addMenu(subfolder_name)
        return subfolder_menu

    def list_files(self, path, menu):
        '''
            Lists txt files in the folder.
        '''
        for file_name in os.listdir(path):
            file_path = path + "/" + file_name
            if os.path.isfile(file_path) is True:
                if file_path[-3:] == "txt":
                    self.add_file_to_menu(file_name, file_path, menu)

    def add_file_to_menu(self, file_name, file_path, menu):
        '''
            Create file in the menu.
        '''
        file_menu = menu.addAction(file_name)
        file_menu.triggered.connect(lambda: self.copy_contents(file_path))

    def copy_contents(self, object_path):
        '''
            Copies the selected files contents to clipboard.
        '''
        with open(object_path, "r") as file:
            txt_to_copy = file.read()
        pyperclip.copy(txt_to_copy)


def main(image, application):
    # application = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon(image), widget)
    tray_icon.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    application = QApplication(sys.argv)
    config = Config()
    image = systray_icon
    main(image, application)
