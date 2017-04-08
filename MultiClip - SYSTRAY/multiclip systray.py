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

    menu_items = []

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        exitAction = menu.addAction("Exit",)
        exitAction.triggered.connect(parent.close)

    def list_subfolders_gui(mc_dir):
        for object in os.listdir(mc_dir):
            object_path = mc_dir + object
            if os.path.isdir(object_path):
                dirEntry = menu.addMenu(object)

    def list_files_gui(mc_dir):
        for object in os.listdir(mc_dir):
            object_path = mc_dir + object
            if os.path.isfile(object_path):
                fileAction = menu.addAction(object)
                fileAction.triggered.connect(self.testing_func)

        self.setContextMenu(menu)

    subfolders = []
    def list_subfolders(path):
        for i in os.listdir(path):
            object_path = path +'/'+ i
            if os.path.isdir(object_path) is True:
                print ">> Folder : ", object_path
                # subfolders.append(object_path)
                self.list_files(object_path)
                print '\n'
                self.list_subfolders(object_path)

    def list_files(path):
         for i in os.listdir(path):
             object_path = path +'/'+ i
             if os.path.isfile(object_path) is True:
                 print object_path


    def testing_func(self):
        snd = self.sender().text()
        print(f"detected: {snd}")


def main(image):
    app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)
    trayIcon.list_subfolders(mc_dir)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    on = r'D:\Python\mc.ico'
    main(on)
