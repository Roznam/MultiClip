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
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QMessageBox, QSystemTrayIcon, QMenu


class Config(object):
    def __init__(self, widget):
        self.source_dir = ''
        self.systray_icon = ''
        self.widget = widget

    def read_config(self):
        '''
            Read config.ini file to set source_dir and systray_icon
        '''
        if os.path.isfile("config.ini"):
            try:
                config = ConfigParser()
                config.read("config.ini")
                self.source_dir = config.get('DEFAULTS', 'MultiClip_Directory')
                self.systray_icon = config.get('DEFAULTS', 'System_Tray_Icon')
                config_status = 1
            except:
                config_status = 0
        else:
            config_status = 0
        return config_status

    def write_config(self):
        '''
            Write config.ini after prompting user for input via popup input box
        '''
        self.get_source_dir()
        self.get_systray_icon()

        with open("config.ini", "w") as file:
            file.write("[DEFAULTS]\nMultiClip_Directory = {0}\nSystem_Tray_Icon = {1}\n".format(self.source_dir, self.systray_icon))

    def get_source_dir(self):
        '''
            Input prompt popup for source_dir, sets value globally for import
            Calls 'popup' if value entered is not a valid directory path
        '''
        text, okPressed = QInputDialog.getText(widget, "Configuration", "MultiClip directory:", QLineEdit.Normal, "")
        if okPressed is True:
            if os.path.isdir(text) is True:
                self.source_dir = text
            else:
                self.popup(0, "Not a valid directory", text)
        else:
            exit()

    def get_systray_icon(self):
        '''
            Check directory for "multiclip.ico"
            If unable to find, ask user to navigate to ico file
        '''
        if os.path.isfile("multiclip.ico"):
            self.systray_icon = "multiclip.ico"
        else:
            text, okPressed = QInputDialog.getText(widget, "Configuration", "MultiClip system tray icon :", QLineEdit.Normal, "")
            if okPressed is True:
                if os.path.isfile(text) is True:
                    if text[-3:].lower() == "ico":
                        self.systray_icon = text
                    else:
                        self.popup(1, "File must be .ico format", text)
                else:
                    self.popup(1, "Not a valid filepath", text)
            else:
                exit()

    def popup(self, function, error, path):
        '''
            Create a warning popup box
        '''
        buttonReply = QMessageBox.warning(widget, 'Config Error',
                                          "{0}: \n{1}".format(error, path), QMessageBox.Ok | QMessageBox.Close)
        if buttonReply == QMessageBox.Ok:
            if function == 0:
                self.get_source_dir()
            elif function == 1:
                self.get_systray_icon()
        if buttonReply == QMessageBox.Close:
            exit()


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, source_dir, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)

        self.list_subfolders(source_dir, menu)
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
            object_path = path + '/' + object_name
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
            file_path = path + '/' + file_name
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


def main(image, source_dir, application, widget):
    tray_icon = SystemTrayIcon(QtGui.QIcon(image), source_dir, widget)
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
    source_dir = config.source_dir
    main(image, source_dir, application, widget)
