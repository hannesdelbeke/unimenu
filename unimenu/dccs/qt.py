from unimenu.dccs._abstract import MenuNodeAbstract
import contextlib


with contextlib.suppress(ImportError):
    from PySide6 import QtGui, QtWidgets
with contextlib.suppress(ImportError):
    from PyQt6 import QtGui, QtWidgets
with contextlib.suppress(ImportError):
    from PySide2 import QtGui, QtWidgets
with contextlib.suppress(ImportError):
    from PyQt5 import QtGui, QtWidgets


class MenuNodeQt(MenuNodeAbstract):

    def _setup_sub_menu(self, parent_app_node=None) -> QtWidgets.QMenu:
        menu = QtWidgets.QMenu(title=self.label)  # parent
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

        action = QtWidgets.QAction(self.label)

        # qt accepts callable commands, not just string commands
        if isinstance(self.command, str):
            action.triggered.connect(lambda: exec(self.command))
        else:  # callable
            action.triggered.connect(lambda: self.command())

        if self.tooltip:
            action.setToolTip(self.tooltip)

        if self.icon:
            # todo test this, krita doesnt support icons
            action.setIconVisibleInMenu(True)
            action.setIcon(QtGui.QIcon(self.icon))

        if parent_app_node:
            parent_app_node.addAction(action)
            action.setParent(parent_app_node)
            # bug? add action doesn't set parent, but addMenu does
            # this makes actions prone to unwanted garbage collection

        return action

    def _setup_separator(self, parent_app_node=None) -> QtWidgets.QAction:
        """
        instantiate a separator object
        """
        action = self._setup_menu_item()
        action.setSeparator(True)
        # todo add label support,
        #  see https://stackoverflow.com/questions/33820789/create-a-separator-with-a-text-in-the-menubar
        return action

    def teardown(self):
        raise NotImplementedError("not yet implemented")
        pass
