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

        for object in os.listdir(mc_dir):
            object_path = mc_dir + object
            if os.path.isdir(object_path):
                dirEntry = menu.addMenu(object)

        for object in os.listdir(mc_dir):
            object_path = mc_dir + object
            if os.path.isfile(object_path):
                fileAction = menu.addAction(object)
                fileAction.triggered.connect(self.testing_func)

        self.setContextMenu(menu)

    def testing_func(self):
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
