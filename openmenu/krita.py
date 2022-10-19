# Krita has native PyQt5 support
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtWidgets import QMenu, QApplication


def setup_menu(data):
    # get main menu as parent
    for widget in QApplication.topLevelWidgets():
        if "MainWindow" in widget.objectName():
            main_window = widget
            break
    main_menu = main_window.findChild(QtWidgets.QMenuBar)

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
