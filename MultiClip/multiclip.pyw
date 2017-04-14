'''
Runs within the system tray -

- Looks at a given folder and creates a nested context on right-click.
- Nested menu will show all folders/files within the parent directory.
- Selecting a folder opens a new nested menu for that folder.
- Selecting a file copies the file contents to the clipboard.
'''

import sys
import os
import pyperclip
from configparser import ConfigParser
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QMessageBox

class Config(QWidget):
    def __init__(self):
        super().__init__()

        if self.read_config() == 1:
            self.read_config()
        else:
            self.write_config()
            self.read_config()


    def initUI(self):
        self.get_mc_dir()
        self.get_systray_icon()

    def get_mc_dir(self):
        '''
            Input prompt popup for mc_dir, sets value globally for import
            Calls 'popup' if value entered is not a valid directory path
        '''
        global mc_dir
        text, okPressed = QInputDialog.getText(self, "Configuration","MultiClip directory:", QLineEdit.Normal, "")
        if okPressed and os.path.isdir(text) is True:
            if text[-1] != "\\":
                mc_dir = text
            else:
                mc_dir = text
        else:
            self.popup("get_mc_dir", "Not a valid directory", text)

    def get_systray_icon(self):
        '''
            Check directory for "multiclip.ico", if unable to find, ask user to navigate to ico file
        '''
        global systray_icon
        if os.path.isfile("multiclip.ico"):
            systray_icon = "multiclip.ico"
        else:
            text, okPressed = QInputDialog.getText(self, "Configuration","MultiClip system tray icon:", QLineEdit.Normal, "")
            if okPressed and os.path.isfile(text) is True:
                if text[-3:].lower() == "ico":
                    systray_icon = text
                else:
                    self.popup("get_systray_icon", "File must be .ico format", text)
            else:
                self.popup("get_systray_icon", "Not a valid filepath", text)

    def popup(self, function, error, path):
        '''
            Create a warning popup box containing: Error, function that called for the popup and invalid path
        '''
        buttonReply = QMessageBox.warning(self, 'Config Error',
                                          f"{error}: \n{path}", QMessageBox.Ok | QMessageBox.Close)
        if buttonReply == QMessageBox.Ok:
            if function == "get_mc_dir":
                self.get_mc_dir()
            elif function == "get_systray_icon":
                self.get_systray_icon()

    def write_config(self):
        '''
            Writes config.ini after prompting user for input via popup input box
        '''
        self.get_mc_dir()
        self.get_systray_icon()

        with open("config.ini", "w") as file:
            file.write(f"[DEFAULTS]\n"
                       f"MultiClip_Directory = {mc_dir}\n"
                       f"System_Tray_Icon = {systray_icon}\n"
                       )

    def read_config(self):
        '''
            Reads config.ini file to set mc_dir and systray_icon
        '''
        config_status = None
        if os.path.isfile("config.ini"):
            try:
                global mc_dir
                global systray_icon
                config = ConfigParser()
                config.read("config.ini")
                mc_dir = config.get('DEFAULTS', 'MultiClip_Directory')
                systray_icon = config.get('DEFAULTS', 'System_Tray_Icon')
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
        exit()

    def list_subfolders(self, path, menu):
        '''
            Detects subfolders, calls file lister for main folder.
            Recursively calls itself for subfolders.
        '''
        for object_name in os.listdir(path):
            object_path = path +'/'+ object_name
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
            file_path = path +'/'+ file_name
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

def main(image):
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    con = QApplication(sys.argv)
    ex = Config()
    on = systray_icon
    main(on)
