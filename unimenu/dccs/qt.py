from unimenu.dccs._abstract import AbstractMenuMaker, MenuNodeAbstract
import contextlib


with contextlib.suppress(ImportError):
    from PySide6 import QtGui, QtWidgets
with contextlib.suppress(ImportError):
    from PyQt6 import QtGui, QtWidgets
with contextlib.suppress(ImportError):
    from PySide2 import QtGui, QtWidgets
with contextlib.suppress(ImportError):
    from PyQt5 import QtGui, QtWidgets


class QtMenuMaker(AbstractMenuMaker):

    @classmethod
    def setup_menu(cls, data, parent):
        return cls._setup_menu_items(parent, [data])

    @classmethod
    def add_sub_menu(cls, parent: QtWidgets.QMenu, label: str) -> QtWidgets.QMenu:
        return parent.addMenu(label)

    @classmethod
    def add_to_menu(cls, parent: QtWidgets.QMenu, label: str, command, icon: str = None, tooltip: str = None):
        if isinstance(command, str):
            action = parent.addAction(label, lambda: exec(command))
        else:  # callable
            action = parent.addAction(label, lambda: command())

        if tooltip:
            parent.setToolTipsVisible(True)
            action.setToolTip(tooltip)

        if icon:
            # todo test this, krita doesnt support icons
            action.setIconVisibleInMenu(True)
            action.setIcon(QtGui.QIcon(icon))

        return action

    @classmethod
    def add_separator(cls, parent, label: str = None) -> "QAction":
        return parent.addSeparator()
        # todo add label support,
        #  see https://stackoverflow.com/questions/33820789/create-a-separator-with-a-text-in-the-menubar

    @classmethod
    def teardown_menu(cls):
        raise NotImplementedError("not yet implemented")


class MenuNodeQt(MenuNodeAbstract):

    def _setup_sub_menu(self, parent_app_node=None):
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

    def _setup_separator(self, parent_app_node=None):
        """
        instantiate a separator object
        """
        action = self._setup_menu_item()
        action.setSeparator(True)
        return action

    def teardown(self):
        raise NotImplementedError("not yet implemented")
        pass
