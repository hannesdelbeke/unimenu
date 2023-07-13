import sys

from Qt import QtWidgets, QtGui, QtCore
import unimenu

config = {
    'label': 'Tools',
    'items':
        [
            {
                'command': 'print("hello 1")',
                'label': 'tool1',
                "icon": ":/qt-project.org/styles/commonstyle/images/up-32.png",
                "tooltip": "tooltip"
            },
            {
                'label': 'label',
                'separator': True,
                "icon": ":/qt-project.org/styles/commonstyle/images/up-32.png",
                "tooltip": "tooltip separator"
            },
            {
                'command': 'print("hello 2")',
                'label': 'tool2'
            },
            {
                'label': 'Tools',
                'items':
                    [
                        {
                            'command': 'print("hello 1")',
                            'label': 'tool1'
                        },
                        {
                            'command': 'print("hello 2")',
                            'label': 'tool2'
                        }
                    ]
            }
        ]

}


class SystemTrayTest(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        super(SystemTrayTest, self).__init__(parent=None)

        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtGui.QColor(255, 0, 0))
        self.setIcon(QtGui.QIcon(pixmap))
        self.show()

        self.main_widget_menu = QtWidgets.QMenu()
        self.main_widget_menu.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.setContextMenu(self.main_widget_menu)
        self.activated.connect(self.show_menu_on_trigger)

        self.app_menu_node = unimenu.setup(config, parent_app_node=self.main_widget_menu)
        self.app_exit = unimenu.setup({"label": "Exit", "command": lambda: sys.exit()},
                                      parent_app_node=self.main_widget_menu)

    def show_menu_on_trigger(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.contextMenu().popup(QtGui.QCursor.pos())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    tray = SystemTrayTest()
    tray.show()
    app.exec_()
