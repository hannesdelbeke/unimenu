# Krita has native PyQt5 support
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QMenu, QApplication
from unimenu.dccs._abstract_qt import AbstractMenuMaker


class MenuMaker(AbstractMenuMaker):
    @classmethod
    def setup_menu(cls, data):
        parent = data.get("parent_menu")

        if not parent:
            # get main menu as parent
            for widget in QApplication.topLevelWidgets():
                if "MainWindow" in widget.objectName():
                    main_window = widget
                    break
            parent = main_window.findChild(QtWidgets.QMenuBar)

        return cls._setup_menu_items(parent, data.get("items"))


setup_menu = MenuMaker.setup_menu
