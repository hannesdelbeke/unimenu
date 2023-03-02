from unimenu.apps._abstract import MenuNodeAbstract
import contextlib


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
class MenuNodeQt(MenuNodeAbstract):

    @property
    def _default_root_parent(self):
        """
        get the default parent for the root node
        it finds the first QMainWindow in the app, and gets its menu bar
        if this is not the desired behaviour, override this method or set the parent of the root node before setup
        """

        # store in global, to avoid garbage collection of python pointer to c++ qt obj
        global menu_bar
        global main_window

        for widget in QtWidgets.QApplication.topLevelWidgets():
            if type(widget) == QtWidgets.QMainWindow:
                main_window = widget
                break

        if not main_window:
            for widget in QtWidgets.QApplication.topLevelWidgets():
                if widget.objectName() == "mainWindow":
                    print("FOUND MAIN WINDOW UNIMENU", main_window)
                    main_window = widget
                    break

        menu_bar = main_window.findChild(QtWidgets.QMenuBar)
        return menu_bar

    def _setup_sub_menu(self, parent_app_node=None) -> QtWidgets.QMenu:
        menu = QtWidgets.QMenu(title=self.label, **self.kwargs)  # parent
        global menu_bar
        if parent_app_node:
            parent_app_node.addMenu(menu)
        return menu

    def _setup_menu_item(self, parent_app_node=None):
        """create a QAction from the MenuNode data"""

        # A PySide.QtGui.QAction may contain an icon, menu text (label), a shortcut, status text,
        # “What’s This?” text, and a tooltip

        # todo support:
        #  openAct.setShortcuts(QKeySequence.Open)
        #  openAct.setStatusTip(tr("Open an existing file"))
        #  PySide.QtGui.QAction.setWhatsThis()
        #  PySide.QtGui.QAction.setFont()

        action = QAction(self.label, **self.kwargs)

        # qt accepts callable commands, not just string commands
        if isinstance(self.command, str):
            action.triggered.connect(lambda: exec(self.command))
        else:  # callable
            action.triggered.connect(lambda: self.command())

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
