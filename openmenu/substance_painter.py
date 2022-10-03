# substance painter has native PySide2 support
import PySide2.QtWidgets as QtWidgets
from PySide2.QtWidgets import QMenu, QApplication

# qwidgets are not exposed in substance it seems
# substance_painter.ui.ApplicationMenu is not a QMenu


# since this is native qt, it's nearly identical to the krita implementation
# TODO can we make a generic qt implementation?

def setup_menu(data):

    # get the raw qt menu
    main_menu = None
    for widget in QApplication.topLevelWidgets():
        if isinstance(widget, QMenu):
            if widget.objectName() == "edit":
                main_menu = widget.parent()

    _setup_menu_items(main_menu, data.get('items'))


def _setup_menu_items(parent_menu, items: list):
    """
    recursively add all menu items and submenus
    """
    for item in items:
        label = item.get('label')
        print(item, label)
        command = item.get('command', None)
        if command:
            add_to_menu(parent_menu, label, command)
        else:  # submenu
            items = item.get('items', [])
            sub_menu = add_sub_menu(parent_menu, label)
            _setup_menu_items(sub_menu, items)


def add_sub_menu(parent: QMenu, label: str) -> QMenu:
    return parent.addMenu(label)


def add_to_menu(parent: QMenu, label: str, command):
    if isinstance(command, str):
        return parent.addAction(label, lambda: exec(command))
    else:  # callable
        return parent.addAction(label, lambda: command())


def breakdown():
    """remove from menu"""
    raise NotImplementedError("not yet implemented")
