from unimenu.dccs._abstract import AbstractMenuMaker, MenuNode
from abc import abstractmethod
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


class QtMenuNode(MenuNode):
    # def __init__(self, label=None, command=None, icon=None, tooltip=None, separator=False, items=None,
    #              parent=None, parent_path=None, app_menu_node=None):
    #     super().__init__(label=label, command=command, icon=icon, tooltip=tooltip, separator=separator, items=items,
    #                      parent=parent, parent_path=parent_path, app_menu_node=app_menu_node)

    # def _parent_app_node(self):
    #     """parent self.app_menu_node to parent.app_menu_node"""
    #     pass

    def _setup_sub_menu(self):
        menu = QtWidgets.QMenu(title=self.label)  # parent
        return menu

        # self.parent.app_menu_node.addMenu(self.label)

    def _setup_menu_item(self):
        """create a QAction from the MenuNode data"""
        command = self.command
        # parent = self.parent.app_menu_node
        icon = self.icon
        tooltip = self.tooltip

        # A PySide.QtGui.QAction may contain an icon, menu text (label), a shortcut, status text,
        # “What’s This?” text, and a tooltip

        # todo support:
        #  openAct.setShortcuts(QKeySequence.Open)
        #  openAct.setStatusTip(tr("Open an existing file"))
        #  PySide.QtGui.QAction.setWhatsThis()
        #  PySide.QtGui.QAction.setFont()

        action = QtWidgets.QAction(self.label)

        # qt accepts callable commands, not just string commands
        if isinstance(command, str):
            action.triggered.connect(lambda: exec(command))
            # action = parent.addAction(label, lambda: exec(command))
        else:  # callable
            # action = parent.addAction(label, lambda: command())
            action.triggered.connect(lambda: command())

        if tooltip:
            # parent.setToolTipsVisible(True)
            action.setToolTip(tooltip)

        if icon:
            # todo test this, krita doesnt support icons
            action.setIconVisibleInMenu(True)
            action.setIcon(QtGui.QIcon(icon))

        return action

    def _setup_separator(self):
        """
        instantiate a separator object
        """
        action = self._setup_menu_item()
        action.setSeparator(True)
        return action

    # @abstractmethod
    # def _teardown(self):
    #     pass
