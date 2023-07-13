import sys

from Qt import QtWidgets, QtGui
import unimenu


class SystemTrayTest(QtWidgets.QMainWindow):
    def __init__(self):
        super(SystemTrayTest, self).__init__(parent=None)
        self.setObjectName('mainWindow')

        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtGui.QColor(255, 0, 0))
        self.tray = QtWidgets.QSystemTrayIcon(None)
        self.tray.setIcon(QtGui.QIcon(pixmap))
        self.tray.show()

        self.main_widget_menu = QtWidgets.QMenu(self)
        self.tray.setContextMenu(self.main_widget_menu)
        self.tray.activated.connect(self.show_menu_on_trigger)

        menu = unimenu.Node(label="test", use_menu_bar=False)
        menu2 = unimenu.Node(label="test1", use_menu_bar=False)
        item1 = unimenu.Node(label="bye", command=lambda: print("Hello"))
        item = unimenu.Node(label="hi")
        sub_item = unimenu.Node(label="test", command=lambda: print("Hello"))
        item.items.append(sub_item)
        menu.items.append(item)
        menu2.items.append(item1)
        menu.setup()
        menu2.setup()

        exit_action = unimenu.Node(label="Exit", command=lambda: sys.exit(), use_menu_bar=False)
        exit_action.setup()

    def show_menu_on_trigger(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.tray.contextMenu().popup(QtGui.QCursor.pos())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tray = SystemTrayTest()
    tray.tray.show()
    app.exec_()
