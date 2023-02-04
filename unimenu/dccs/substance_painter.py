# substance painter has native PySide2 support
import PySide2.QtWidgets as QtWidgets
from PySide2.QtWidgets import QMenu, QApplication
from unimenu.dccs.qt import QtMenuMaker, MenuNodeQt

# it seems substance's native UI qwidgets aren't accessible
# substance_painter.ui.ApplicationMenu is not a QMenu


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


class MenuNodeSubstance(MenuNodeQt):
    @property
    def _default_root_parent(self):
        """get the default parent for the root node, optional method"""
        return main_menu_bar()
