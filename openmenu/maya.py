import pymel.core as pm
import json
import warnings
from pathlib import Path
import sys


def setup(path: (str, Path)):
    """setup menu"""
    path = str(path)
    if path.lower().endswith('.json'):
        return setup_from_json(path)
    elif path.lower().endswith('.yaml'):
        return setup_from_yaml(path)


def setup_from_json(config_path):
    with open(config_path) as file:
        data = json.load(file)
    return setup_menu(data)


def setup_from_yaml(config_path):
    import yaml

    with open(config_path) as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return setup_menu(data)


def setup_menu(data):
    # parent_menu_name = data.get('parent_menu')  # LevelEditor.MainMenu
    # unreal_menus = unreal.ToolMenus.get()
    # parent_menu = unreal_menus.find_menu(parent_menu_name)
    # if not parent_menu:
    #    warnings.warn(f"Parent menu '{parent_menu_name}' not found, couldn't setup menu")
    parent_menu = None
    _setup_menu_items(parent_menu, data.get('items'))
    # unreal_menus.refresh_all_widgets()
    # TODO decide to return success/failure, or the menu object


def _setup_menu_items(parent_menu, items: list):
    # go over all items in the menu and add them to the menu
    # if there are subitems, call self on data recursively
    for item in items:
        name = item.get('name')
        command = item.get('command', None)
        if command:
            add_to_menu(parent_menu, name, command)
        else:  # submenu
            items = item.get('items', [])
            sub_menu = add_sub_menu(parent_menu, name)
            _setup_menu_items(sub_menu, items)


def add_sub_menu(script_menu, label: str):
    if not script_menu:  # setup root menu
        MainMayaWindow = pm.language.melGlobals['gMainWindow']
        return pm.menu(label, parent=MainMayaWindow)
    return pm.menuItem(subMenu=True, label=label, parent=script_menu)


def add_to_menu(script_menu, label: str, command: str):
    print("add menu command", script_menu, label, command)
    return pm.menuItem(label=label, command=command, parent=script_menu)


def breakdown():
    """remove from menu"""
    raise NotImplementedError("not yet implemented")