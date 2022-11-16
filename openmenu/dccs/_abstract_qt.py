from openmenu.dccs._abstract import AbstractMenuMaker
from abc import abstractmethod
import contextlib


with contextlib.suppress(ImportError):
    from PySide2.QtGui import QIcon
with contextlib.suppress(ImportError):
    from PyQt5.QtGui import QIcon


class AbstractMenuMaker(AbstractMenuMaker):
    @classmethod
    @abstractmethod
    def setup_menu(cls, data):
        pass

    @classmethod
    def add_sub_menu(cls, parent: "QMenu", label: str) -> "QMenu":
        return parent.addMenu(label)

    @classmethod
    def add_to_menu(cls, parent: "QMenu", label: str, command, icon: str = None, tooltip: str = None):
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
            action.setIcon(QIcon(icon))

        return action

    @classmethod
    def add_separator(cls, parent) -> "QAction":
        return parent.addSeparator()

    @classmethod
    def teardown_menu(cls):
        raise NotImplementedError("not yet implemented")
