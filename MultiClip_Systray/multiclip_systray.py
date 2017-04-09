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
from PyQt5 import QtCore, QtGui, QtWidgets
from config import config, mc_dir, systray_icon

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
            Lists files in the folder.
        '''
        for file_name in os.listdir(path):
            file_path = path +'/'+ file_name
            if os.path.isfile(file_path) is True:
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
    config()
    on = systray_icon
    main(on)
