# substance painter has native PySide2 support
import PySide2.QtWidgets as QtWidgets
from PySide2.QtWidgets import QMenu, QApplication
from unimenu.dccs._abstract_qt import AbstractMenuMaker

# it seems substance's native UI qwidgets aren't accessible
# substance_painter.ui.ApplicationMenu is not a QMenu


class MenuMaker(AbstractMenuMaker):
    @classmethod
    def setup_menu(cls, data):
        parent = data.get("parent_menu")

        if not parent:
            # get the raw qt menu
            main_menu = None
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, QMenu):
                    if widget.objectName() == "edit":
                        main_menu = widget.parent()
            parent = main_menu

        return cls._setup_menu_items(parent, data.get("items"))


setup_menu = MenuMaker.setup_menu
