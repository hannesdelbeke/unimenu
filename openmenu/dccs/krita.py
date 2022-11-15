# Krita has native PyQt5 support
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QMenu, QApplication
from openmenu.dccs._abstract import AbstractMenuMaker


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

        return cls._setup_menu_items(parent, data.get('items'))

    @classmethod
    def add_sub_menu(cls, parent: QMenu, label: str) -> QMenu:
        return parent.addMenu(label)

    @classmethod
    def add_to_menu(cls, parent: QMenu, label: str, command, icon: str = None, tooltip: str = None):
        if isinstance(command, str):
            return parent.addAction(label, lambda: exec(command))
        else:  # callable
            return parent.addAction(label, lambda: command())

    @classmethod
    def add_separator(cls, parent) -> "QAction":
        return parent.addSeparator()

    @classmethod
    def teardown_menu(cls):
        raise NotImplementedError("not yet implemented")

setup_menu = MenuMaker.setup_menu
