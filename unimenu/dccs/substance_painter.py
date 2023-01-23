# substance painter has native PySide2 support
import PySide2.QtWidgets as QtWidgets
from PySide2.QtWidgets import QMenu, QApplication
from unimenu.dccs.qt import QtMenuMaker

# it seems substance's native UI qwidgets aren't accessible
# substance_painter.ui.ApplicationMenu is not a QMenu


class MenuMaker(QtMenuMaker):
    @classmethod
    def setup_menu(cls, data):
        parent = data.get("parent_menu") or main_menu_bar()
        return cls._setup_menu_items(parent, data.get("items"))


setup_menu = MenuMaker.setup_menu


# todo can we move this to qt class. inherit get_main_menu_bar for all DCCs
#  overwrite if needed
def main_menu_bar() -> QtWidgets.QMenuBar:
    # get the raw qt menu
    main_menu = None
    for widget in QApplication.topLevelWidgets():
        if isinstance(widget, QMenu):
            if widget.objectName() == "edit":
                main_menu = widget.parent()
    return main_menu
