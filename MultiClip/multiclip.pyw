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
import win32com.client
from win32com.client import Dispatch
from configparser import ConfigParser
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QMessageBox

mc_dir = ""


class Config(QWidget):
    def __init__(self):
        super().__init__()

        config_status = self.read_config()
        if config_status == 0:
            self.get_mc_dir()
            self.write_config()
            self.read_config()

    def read_config(self):
        '''
            Read config.ini file to set mc_dir and systray_icon
            Calls get_systray_icon
        '''
        global mc_dir
        if os.path.isfile("config.ini"):
            try:
                systray_icon = self.get_systray_icon()
                config = ConfigParser()
                config.read("config.ini")
                mc_dir = config.get("DEFAULTS", "MultiClip_Directory")
                config_status = 1
            except:
                config_status = 0
        else:
            config_status = 0
        return config_status

    def get_systray_icon(self):
        '''
            Set systray variable to icon included with PyInstaller
        '''
        return self.get_absolute_path("multiclip.ico")

    def get_absolute_path(self, relative_path):
        '''
            Get absolute path to resource, works for dev and for PyInstaller
        '''
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def write_config(self):
        '''
            Write config.ini after prompting user for input via popup input box
        '''
        with open("config.ini", "w") as file:
            file.write("[DEFAULTS]\nMultiClip_Directory = %s\n" % mc_dir)

    def get_mc_dir(self):
        '''
            Input prompt popup for mc_dir, sets value globally for import
            Calls 'popup' if value entered is not a valid directory path
        '''
        global mc_dir
        text, okPressed = QInputDialog.getText(self, "Configuration", "MultiClip directory:", QLineEdit.Normal, "")
        if okPressed and os.path.isdir(text) is True:
            mc_dir = text
        else:
            self.popup(0, "Not a valid directory", text)

    def popup(self, function, error, path):
        '''
            Create a warning popup box containing: Error, function that called for the popup and invalid path
        '''
        buttonReply = QMessageBox.warning(self, "Config Error",
                                          ("%s: \n" % error) + ("%s" % path), QMessageBox.Ok | QMessageBox.Close)
        if buttonReply == QMessageBox.Ok:
            if function == 0:
                self.get_mc_dir()
        if buttonReply == QMessageBox.Close:
            exit()


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
            Detects subfolders, and folder shortcuts calls file lister for main folder.
            Recursively calls itself for subfolders.
        '''
        for object_name in os.listdir(path):
            object_path = path + "/" + object_name
            if os.path.isdir(object_path) is True:
                subfolder_menu = self.create_submenu(object_name, menu)
                self.list_subfolders(object_path, subfolder_menu)
            if object_path[-4:] == ".lnk":
                shell = Dispatch("WScript.Shell")
                shortcut = (shell.CreateShortcut(object_path)).Targetpath
                if os.path.isdir(shortcut) is True:
                    subfolder_menu = self.create_submenu(object_name[:-4], menu)
                    self.list_subfolders(shortcut, subfolder_menu)
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
    widget = QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon(image), widget)
    tray_icon.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    application = QApplication(sys.argv)
    config = Config()
    image = config.get_systray_icon()
    main(image, application)
