from openmenu.dccs._abstract import AbstractMenuMaker
from abc import abstractmethod


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
            return parent.addAction(label, lambda: exec(command))
        else:  # callable
            return parent.addAction(label, lambda: command())

    @classmethod
    def add_separator(cls, parent) -> "QAction":
        return parent.addSeparator()

    @classmethod
    def teardown_menu(cls):
        raise NotImplementedError("not yet implemented")
