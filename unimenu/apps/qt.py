from unimenu.apps._abstract import MenuNodeAbstract
import contextlib
import logging


with contextlib.suppress(ImportError):
    from PySide6 import QtGui, QtWidgets
    from PySide6.QtGui import QAction
with contextlib.suppress(ImportError):
    from PyQt6 import QtGui, QtWidgets
    from PyQt6.QtGui import QAction
with contextlib.suppress(ImportError):
    from PySide2 import QtGui, QtWidgets
    from PySide2.QtWidgets import QAction
with contextlib.suppress(ImportError):
    from PyQt5 import QtGui, QtWidgets
    from PyQt5.QtWidgets import QAction


menu_bar = None
main_window = None


def find_main_window():
    # ideally there is only 1 main window, but there could be more
    # e.g. Maya has a main window for arnold
    widgets = [w for w in QtWidgets.QApplication.topLevelWidgets() if type(w) == QtWidgets.QMainWindow]
    if len(widgets) == 1:
        return widgets[0]
    else:
        logging.warning(f"found {len(widgets)} main windows,  can't auto select main window")

    # a lot of apps have a main window named "mainWindow"
    if not main_window:
        for widget in QtWidgets.QApplication.topLevelWidgets():
            if widget.objectName() in ("mainWindow", "MayaWindow"):  # MayaWindow hardcode hack
                # print("FOUND MAIN WINDOW UNIMENU", main_window)
                return widget


def find_main_menu_bar(main_window, parent_path):
    """
    get the main menu bar widget from a main window,
    or the sub menu widget if a sub path is provided
    """
    menu_bar = main_window.findChild(QtWidgets.QMenuBar)
    if parent_path:
        parent_menu = menu_bar.findChild(QtWidgets.QMenu, parent_path)
        if not parent_menu:
            logging.warning("Parent menu not found, using main menu bar")
        else:
            menu_bar = parent_menu
    return menu_bar


class MenuNodeQt(MenuNodeAbstract):
    @property
    def _default_root_parent(self):
        """
        get the default parent for the root node
        it finds the first QMainWindow in the app, and gets its menu bar
        if this is not the desired behaviour, override this method or set the parent of the root node before setup
        """
        # store in global, to avoid garbage collection of python pointer to c++ qt obj
        global main_window
        global menu_bar

        main_window = find_main_window()
        menu_bar = find_main_menu_bar(main_window, self.parent_path)
        return menu_bar

    def _setup_sub_menu(self, parent_app_node=None) -> QtWidgets.QMenu:
        menu = QtWidgets.QMenu(title=self.label, objectName=self.id, parent=parent_app_node, **self.kwargs)
        if parent_app_node:
            parent_app_node.addMenu(menu)
        return menu

    def _setup_menu_item(self, parent_app_node=None) -> QAction:
        """
        create a QAction from the MenuNode data
        parent_app_node: the parent menu or menu bar
        """

        # A PySide.QtGui.QAction may contain an icon, menu text (label), a shortcut, status text,
        # “What’s This?” text, and a tooltip

        # todo support:
        #  openAct.setShortcuts(QKeySequence.Open)
        #  openAct.setStatusTip(tr("Open an existing file"))
        #  PySide.QtGui.QAction.setWhatsThis()
        #  PySide.QtGui.QAction.setFont()

        action = QAction(self.label, objectName=self.id, **self.kwargs)
        action.triggered.connect(self.run)

        if self.tooltip:
            if parent_app_node:
                parent_app_node.setToolTipsVisible(True)
            action.setToolTip(self.tooltip)

        if self.icon:
            action.setIconVisibleInMenu(True)
            action.setIcon(QtGui.QIcon(self.icon))

        if parent_app_node:
            parent_app_node.addAction(action)
            action.setParent(parent_app_node)
            # bug? add action doesn't set parent, but addMenu does
            # this makes actions prone to unwanted garbage collection

        return action

    def _setup_separator(self, parent_app_node=None) -> QAction:
        """
        instantiate a separator object
        """
        action = self._setup_menu_item(parent_app_node=parent_app_node)
        action.setSeparator(True)
        return action

    def teardown(self):
        """remove from menu"""
        self.app_node.deleteLater()
