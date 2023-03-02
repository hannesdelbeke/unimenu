"""
native maya menu support. not needed anymore, use the qt menu instead
"""

import pymel.core as pm  # todo replace with cmds because it's faster
from unimenu.apps._abstract import MenuNodeAbstract
import maya.mel
import maya.cmds


counter = 0


def get_counter():
    global counter
    counter += 1
    return counter


def find_menu(name):
    gMainWindow = maya.mel.eval('$temp=$gMainWindow')
    # get all the menus that are children of the main menu
    mainWindowMenus = maya.cmds.window(gMainWindow, query=True, menuArray=True)
    for menu in mainWindowMenus:
        if menu.lower() == name.lower():
            return menu

        # TODO get their children recursively


def create_root_menu(label, window_name=None, kwargs=None) -> pm.menu:
    """
    Create a root menu in Maya
    label: str, the label of the menu
    window_name: str, the name of the window to attach the menu to
    """
    window_name = window_name or "gMainWindow"  # default value
    maya_window = pm.language.melGlobals[window_name]

    # support adding custom kwargs from the config
    kwargs = kwargs or {}
    kwargs.setdefault("parent", maya_window)
    kwargs.setdefault("tearOff", True)

    # we require a predictable name to parent menus to from other configs, so no counter
    # name = f"{label}_{get_counter()}"
    name = label.replace("_", " ")  # maya menu names can't have underscores

    return pm.menu(name, **kwargs)


class MenuNodeMaya(MenuNodeAbstract):

    @property
    def _default_root_parent(self):

        # todo parent logic currently is re implemented in every app module
        #  can we move it to the abstract class?
        # if we provide a parent in the config, we might want to parent to a submenu
        if self.parent_path:
            parent_path = self.parent_path.replace(" ", "_")  # maya menu names can't have spaces
            return find_menu(parent_path)

    def _setup_sub_menu(self, parent_app_node=None):
        # todo handle unique name, atm label can clash with other menu items

        # support adding custom kwargs from the config
        kwargs = self.kwargs
        kwargs.setdefault("tearOff", True)

        if not parent_app_node:
            return create_root_menu(self.label, kwargs=self.kwargs)
        else:  # make a normal sub menu
            kwargs.setdefault("subMenu", True)
            kwargs.setdefault("label", self.label)
            kwargs.setdefault("parent", parent_app_node)

            self.name = f"{self.label}_{get_counter()}"
            return pm.menuItem(self.name, **kwargs)

    def _setup_menu_item(self, parent_app_node=None):
        icon = self.icon or ""

        # tooltip = self.tooltip or ""
        # todo menuItem doesn't support tooltip.
        #  could use qt instead http://discourse.techart.online/t/is-there-a-way-to-get-tooltips-for-maya-menitem/15385

        # support adding custom kwargs from the config
        kwargs = self.kwargs
        kwargs.setdefault("label", self.label)
        kwargs.setdefault("command", self.try_command)
        kwargs.setdefault("parent", parent_app_node)
        kwargs.setdefault("image", icon)

        self.name = f"{self.label}_{get_counter()}"

        return pm.menuItem(self.name, **kwargs)

    def _setup_separator(self, parent_app_node=None):
        self.name = f"{self.label}_{get_counter()}"

        # support adding custom kwargs from the config
        kwargs = self.kwargs
        kwargs.setdefault("divider", True)
        kwargs.setdefault("dividerLabel", self.label)
        kwargs.setdefault("parent", parent_app_node)

        return pm.menuItem(self.name, **kwargs)

    def teardown(self):
        # see https://stackoverflow.com/questions/44142119/remove-menu-item-in-maya-using-python
        # todo can we remove self.name? bit hacky
        pm.deleteUI(self.name, menu=True)
