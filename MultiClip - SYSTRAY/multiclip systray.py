import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets

mc_dir = "D:\\Python\\MC\\"

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(parent.close)

        self.list_subfolders(mc_dir, menu)

        self.setContextMenu(menu)

    subfolders = []

    def list_subfolders(self, path, menu):
        for i in os.listdir(path):
            object_path = path +'/'+ i
            if os.path.isdir(object_path) is True:
                print (">> Folder : ", object_path)
                subfolder_menu = self.create_submenu(i, menu)
                #subfolders.append(object_path)
                #self.list_files(object_path)
                print ('\n')
                self.list_subfolders(object_path, subfolder_menu)

    def list_files(self, path):
         for i in os.listdir(path):
             object_path = path +'/'+ i
             if os.path.isfile(object_path) is True:
                 print (object_path)

    def create_submenu(self, i, menu):
        subfolder_menu = menu.addMenu(i)
        return subfolder_menu

def main(image):
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    on=r'D:\Python\mc.ico'
    main(on)
