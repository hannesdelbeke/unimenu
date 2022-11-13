import json
import warnings
from pathlib import Path
from collections import namedtuple
import importlib
import pkgutil
import contextlib
from typing import Union, Optional

__all__ = [
    'DCC',
    'DCCs',
    # 'setup',
    'setup_config',
    'setup_dict',
    'setup_module',
    'add_item',
    # 'breakdown',
    ]


# name: the name of the dcc, and also the name of the menu module
# name of module: a unique python module only available in that dcc
# callback: not sure if we need this
DCC = namedtuple('DCC', ['name', 'module'])


class DCCs:
    """DCCs supported by this module"""

    # dcc -> digital content creation (software)

    BLENDER = DCC('blender', 'bpy')
    MAYA = DCC('maya', 'maya')  # pymel can be slow to import
    UNREAL = DCC('unreal', 'unreal')
    MAX = DCC('max', 'pymxs')
    KRITA = DCC('krita', 'krita')
    SUBSTANCE_DESIGNER = DCC('substance_designer', 'pysbs')
    SUBSTANCE_PAINTER = DCC('substance_painter', 'substance_painter')
    MARMOSET = DCC('marmoset', 'mset')

    ALL = [BLENDER, MAYA, UNREAL, KRITA, SUBSTANCE_PAINTER, MAX, MARMOSET]


def _detect_dcc() -> Optional[DCC]:
    """detect which dcc is currently running"""
    for dcc in DCCs.ALL:
        with contextlib.suppress(ImportError):
            __import__(dcc.module)
            print(f"OPENMENU: detected {dcc.name}")
            return dcc
    warnings.warn("OPENMENU: no supported DCC detected")


def _get_json_data(config_path):
    """get json data from a file path, return None if not json"""
    path = str(config_path)
    if not path.lower().endswith('.json'):
        return

    with open(config_path) as file:
        data = json.load(file)
    return data


def _get_yaml_data(config_path):
    """get yaml data from a file path, return None if not yaml"""
    path = str(config_path)
    if not path.lower().endswith('.yaml'):
        return

    import yaml

    with open(config_path) as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return data


def _getattr_recursive(obj, attr: str):
    """
    getattr but recursive, supports nested attributes
    attr: provide either 1 attribute, or multiple separated by a dot
    """
    attributes = attr.split('.')
    for attribute in attributes:
        obj = getattr(obj, attribute)
    return obj


def setup_config(path: Union[str, Path], dcc=None):
    """menu setup from a json or yaml file"""
    data = _get_json_data(path) or _get_yaml_data(path)
    return setup(data, dcc)


def setup_dict(data, dcc=None):
    """menu setup from a dict"""
    dcc = dcc or _detect_dcc()
    module = importlib.import_module(f'openmenu.{dcc.name}')
    return module.setup_menu(data)


def setup_module(parent_module_name, parent_menu_name='', menu_name="", function_name='main', dcc=None):
    """
    Create a menu from a folder with modules,
    automatically keep your menu up to date with all tools in that folder

    note: ensure the folder is importable and in your environment path

    Args:
    parent_module_name: the name of the module that contains all tools. e.g.: "cool_tools"
                        cool_tools
                        ├─ __init__.py   (import cool_tools)
                        ├─ tool1.py      (import cool_tools.tool1)
                        └─ tool2.py      (import cool_tools.tool2)
    parent_menu_name: the name of the parent menu to add our menu entries to
    menu_name: optional kwars to overwrite the name of the menu to create, defaults to module name
    function_name: the function name to run on the module, e.g.: 'run', defaults to 'main'
                   if empty, call the module directly
    dcc: the dcc that contains the menu. if None, will try to detect dcc
    """

    parent_module = importlib.import_module(parent_module_name)

    # create dict for every module in the folder
    # label: the name of the module
    # callback: the function to run

    # todo support recursive folders -> auto create submenus

    items = []
    for module_finder, submodule_name, ispkg in pkgutil.iter_modules(parent_module.__path__):

        # skip private modules
        if submodule_name.startswith('_'):
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
                function = _getattr_recursive(submodule, _function_name)
                function()
            else:
                submodule()

        submodule_dict = {
            'label': submodule_name,
            'command': callback,
        }
        items.append(submodule_dict)

    data = {}
    if parent_menu_name:
        data['parent'] = parent_menu_name
    data['items'] = [{'label': menu_name or parent_module.__name__, 'items': items}]

    # use the generated dict to set up the menu
    return setup(data, dcc)


def add_item(label, command=None, parent=None, icon_name=None):
    """
    add a menu entry to the dcc menu

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
    if icon_name:
        data['items'][0]['icon'] = icon_name
    if command:
        data['items'][0]['command'] = command
    if parent:
        data['parent_menu'] = parent
    return setup(data)


def breakdown():
    """remove the create menu"""
    # todo module.breakdown()
    raise NotImplementedError("not yet implemented")


# backwards compatibility
setup = setup_dict
module_setup = setup_module
config_setup = setup_config

