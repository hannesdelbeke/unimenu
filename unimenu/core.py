"""
Core methods to generate custom menus.
"""

from pathlib import Path
import importlib
import pkgutil
from typing import Union
from unimenu.dccs import detect_dcc, DCC
from unimenu.utils import get_json_data, get_yaml_data, getattr_recursive


def setup_dict(data, dcc: DCC = None):
    """menu setup from a dict"""
    dcc = dcc or detect_dcc()
    return dcc.menu_module.setup_menu(data)


def setup_config(config_path: Union[str, Path], dcc: DCC = None):
    """menu setup from a json or yaml file"""
    data = get_json_data(config_path) or get_yaml_data(config_path)
    return setup_dict(data, dcc)


def setup_module(module, parent_menu="", menu_name="", function_name="main", icon="", tooltip="", dcc=None, smart_spaces=True):
    """
    Create a menu from a folder with modules,
    automatically keep your menu up to date with all tools in that folder

    note: ensure the folder is importable and in your environment path

    Args:
    module: the name of the module that contains all tools. e.g.: "cool_tools"
                        cool_tools
                        ├─ __init__.py   (import cool_tools)
                        ├─ tool1.py      (import cool_tools.tool1)
                        └─ tool2.py      (import cool_tools.tool2)
    parent: the name of the parent menu to add our menu entries to
    menu_name: optional kwars to overwrite the name of the menu to create, defaults to module name
    function_name: the function name to run on the module, e.g.: 'run', defaults to 'main'
                   if empty, call the module directly
    icon: the icon name to use for the menu entry, defaults to ''
    dcc: the dcc that contains the menu. if None, will try to detect dcc
    """

    parent_module = importlib.import_module(module)

    # create dict for every module in the folder
    # label: the name of the module
    # callback: the function to run

    # todo support recursive folders -> auto create submenus

    items = []
    for module_finder, submodule_name, ispkg in pkgutil.iter_modules(parent_module.__path__):

        # skip private modules
        if submodule_name.startswith("_"):
            continue

        # to prevent issues with late binding
        # https://stackoverflow.com/questions/3431676/creating-functions-or-lambdas-in-a-loop-or-comprehension
        # first arg might be self, e.g. operator wrapped in blender
        def callback(self=None, _submodule_name=submodule_name, _function_name=function_name, *args, **kwargs):

            # only import the module after clicking in the menu
            # so failed module imports don't break the menu setup
            submodule = module_finder.find_spec(_submodule_name).loader.load_module()

            # run the user-provided function on the module, or call the module directly
            if _function_name:
                function = getattr_recursive(submodule, _function_name)
                function()
            else:
                submodule()

        # add spaces to the label. e.g.: "my_tool" -> "My Tool"
        submodule_label = submodule_name.replace('_', ' ').title() if smart_spaces else submodule_name

        submodule_dict = {
            "label": submodule_label,
            "command": callback,  # todo ensure this also works for dccs that only support strings
        }
        if icon:
            submodule_dict["icon"] = icon
        if tooltip:
            submodule_dict["tooltip"] = tooltip
        items.append(submodule_dict)

    data = {}
    if parent_menu:
        data["parent"] = parent_menu
    data["items"] = [{"label": menu_name or parent_module.__name__, "items": items}]

    # use the generated dict to set up the menu
    return setup_dict(data, dcc)


# def add_separator(parent, label: str = None):
#     # todo explain what this does
#     data = {
#         "items": ["---"],
#         "parent": parent,
#         "label": label,
#     }
#     return setup_dict(data)


def add_item(label, command=None, parent=None, icon=None, tooltip=None):
    """
    add a single menu entry to the dcc menu

    Args:
        label: the label of the menu entry, defaults to None
        command: the command to run when the menu entry is clicked, defaults to None
                 some dccs support callbacks, but most use string commands
                 if None, the menu is seen as a submenu.
        parent: the parent menu name to add the entry to, defaults to None
        icon_name: the name of the icon to use, defaults to None
        todo add menu entry name support, defaults to using label, so no duplicate names currently
    """
    data = {
        "items": [
            {
                "label": label,
            }
        ]
    }
    if icon:
        data["items"][0]["icon"] = icon
    if command:
        data["items"][0]["command"] = command
    if parent:
        data["parent"] = parent
    if tooltip:
        data["items"][0]["tooltip"] = tooltip
    return setup_dict(data)[0]


def teardown_config(config_path):
    """remove the created menu"""
    # get all entries from a config, assume they are setup, and attempt a teardown
    data = get_json_data(config_path) or get_yaml_data(config_path)
    return teardown_dict(data)


def teardown_dict(data, dcc=None):
    """remove the created menu"""
    # get all entries from a dict, assume they are setup, and attempt a teardown
    dcc = dcc or detect_dcc()
    return dcc.menu_module.teardown_menu(data)
