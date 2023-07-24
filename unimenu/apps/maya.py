"""
native maya menu support. not needed anymore, use the qt menu instead
short menu names are the name of the menu node.
long menu names are the name of the menu, and all its parents, separated by "|"
"""
from unimenu.apps._abstract import MenuNodeAbstract
import maya.mel
import maya.cmds  # cmds is faster than pymel
import re


def find_menu(long_name):
    long_name = f"MayaWindow|{long_name}"  # for now we assume the menu is a child of the main window
    long_menu_names = maya.cmds.lsUI(menus=True, long=True)
    for long_menu_name in long_menu_names:
        if long_menu_name == long_name:
            return long_menu_name


def get_compatible_name(name):
    name = re.sub('[^0-9a-zA-Z]+', '_', name)  # replace non alpha-numeric with _
    name = name.strip("_")  # remove leading and trailing underscores
    return name


def get_unique_name(name, parent):
    """
    Guarantee a unique name compatible with maya naming conventions
    name: str, the short name of the menu
    parent: str, the long name of the parent menu
    """
    name = get_compatible_name(name)
    long_name = f"{parent}|{name}"
    long_menu_names = maya.cmds.lsUI(menus=True, long=True)
    long_menu_item_names = maya.cmds.lsUI(menuItems=True, long=True)
    if any(long_name == long_menu_name for long_menu_name in long_menu_names + long_menu_item_names):
        # if the name is already taken, add a number to the end
        # this could be improved by finding the next available number
        name = f"{name}_1"
        name = get_unique_name(name, parent)
    return name


def create_root_menu(label, window_name=None, kwargs=None) -> maya.cmds.menu:
    """
    Create a root menu in Maya
    label: str, the label of the menu
    window_name: str, the name of the window to attach the menu to
    """
    # todo add support for menus in other windows, e.g. the Script Editor
    # # lsUI() might be able to replace pymel
    # import pymel.core as pm
    # window_name = window_name or "gMainWindow"  # default value
    # maya_window = pm.language.melGlobals[window_name]  # returns "MayaWindow", type str
    # same result as this
    # maya_window = maya.mel.eval('$temp=$gMainWindow')
    maya_window = "MayaWindow"  # hardcode main window for now

    # support adding custom kwargs from the config
    kwargs = kwargs or {}
    kwargs.setdefault("parent", maya_window)
    kwargs.setdefault("tearOff", True)

    name = label.replace("_", " ")  # maya menu labels should have spaces, not underscores

    return maya.cmds.menu(name, **kwargs)


class MenuNodeMaya(MenuNodeAbstract):

    @property
    def _default_root_parent(self):
        # todo parent logic currently is re implemented in every app module
        #  can we move it to the abstract class?
        # if we provide a parent in the config, we might want to parent to a submenu
        if self.parent_path:
            parent_path = get_compatible_name(self.parent_path)
            return find_menu(parent_path)

    def _setup_sub_menu(self, parent_app_node=None):
        self.name = get_unique_name(self.label, parent=parent_app_node)
        kwargs = self.kwargs  # support adding custom kwargs from the config
        kwargs.setdefault("tearOff", True)
        if not parent_app_node:
            return create_root_menu(self.label, kwargs=self.kwargs)
        else:  # make a normal sub menu
            kwargs.setdefault("subMenu", True)
            kwargs.setdefault("label", self.label)
            kwargs.setdefault("parent", parent_app_node)
            return maya.cmds.menuItem(self.name, **kwargs)

    def _setup_menu_item(self, parent_app_node=None):
        self.name = get_unique_name(self.label, parent=parent_app_node)
        icon = self.icon or ""
        tooltip = self.tooltip or "test"
        kwargs = self.kwargs  # support adding custom kwargs from the config
        kwargs.setdefault("label", self.label)
        kwargs.setdefault("command", self.run)
        kwargs.setdefault("parent", parent_app_node)
        kwargs.setdefault("image", icon)
        kwargs.setdefault("annotation", tooltip)  # shown on hover in lower left corner
        return maya.cmds.menuItem(self.name, **kwargs)

    def _setup_separator(self, parent_app_node=None):
        self.name = get_unique_name(self.label, parent=parent_app_node)
        kwargs = self.kwargs  # support adding custom kwargs from the config
        kwargs.setdefault("divider", True)
        kwargs.setdefault("dividerLabel", self.label)
        kwargs.setdefault("parent", parent_app_node)
        return maya.cmds.menuItem(self.name, **kwargs)

    def teardown(self):
        """Delete the menu item & its children"""
        maya.cmds.deleteUI(self.name, menu=True)

