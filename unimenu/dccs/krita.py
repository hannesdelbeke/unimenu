# Krita has native PyQt5 support
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QMenu, QApplication
from unimenu.dccs.qt import MenuNodeQt


class MenuNodeKrita(MenuNodeQt):
    @property
    def _default_root_parent(self):
        """get the default parent for the root node, optional method"""
        return krita_main_menu_bar()


# todo test root parent path in config


def krita_main_menu_bar() -> QtWidgets.QMenuBar:
    """get the main menu widget by name from Krita"""
    for widget in QApplication.topLevelWidgets():
        if "MainWindow" in widget.objectName():
            main_window = widget
            break
    return main_window.findChild(QtWidgets.QMenuBar)
