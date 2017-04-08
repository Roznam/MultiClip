'''
Intended to run within the system tray -

- Looks at a given folder and creats a nested menu context menu when clicking.
- Nested menu will show all folders/files within the parent directory.
- Selecting a folder will open a new nested menu for that folder.
- Selecting a file will copy the file contents to the clipboard.
'''

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets

mc_dir = "D:\\Python\\MC\\"


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)

        self.create_exit(menu)
        self.list_subfolders(mc_dir, menu)
        self.setContextMenu(menu)
    
    def create_exit(self, menu):
        '''
            Creates exit option in menu.
        '''
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(parent.close)

    def list_subfolders(self, path, menu=menu):
        '''
            Detects subfolders, calls file lister for main folder.
            Recursively calls itself for subfolders.
        '''
        for i in os.listdir(path):
            object_path = path +'/'+ i
            if os.path.isdir(object_path) is True:
                subfolder_menu = self.create_submenu(i, menu)
                self.list_files(object_path)
                self.list_subfolders(object_path, subfolder_menu)

    def list_files(self, path):
        '''
        Lists files in the folder.
        '''
         for i in os.listdir(path):
             object_path = path +'/'+ i
             if os.path.isfile(object_path) is True:
                 print object_path
                 self.create_file_in_menu(i, menu)
         print '\n'
    
    def create_submenu(self, i, menu):
        '''
        Create submenu in the menu for subfolder.
        '''
        print ">> Folder : ", object_path
        subfolder_menu = menu.addMenu(i)
        return subfolder_menu

    def create_file_in_menu(self, i, menu):
        '''
        Create file in the menu.
        '''
        file_menu = menu.addAction(i)
        file_menu.triggered.connect(self.testing_func)


    def testing_func(self):
        '''
        Till the actual functionality is added.
        '''
        snd = self.sender().text()
        print(f"detected: {snd}")


def main(image):
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    on = r'D:\Python\mc.ico'
    main(on)
