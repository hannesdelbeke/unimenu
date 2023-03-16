"""
native maya menu support. not needed anymore, use the qt menu instead
"""
from unimenu.apps._abstract import MenuNodeAbstract
import maya.mel
import maya.cmds  # cmds is faster than pymel


def find_menu(name):
    gMainWindow = maya.mel.eval('$temp=$gMainWindow')
    # get all the menus that are children of the main menu
    mainWindowMenus = maya.cmds.window(gMainWindow, query=True, menuArray=True)
    for menu in mainWindowMenus:
        if menu.lower() == name.lower():
            return menu

        # TODO get their children recursively


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
    maya_window = "MayaWindow"  # hardcode main window for now

    # support adding custom kwargs from the config
    kwargs = kwargs or {}
    kwargs.setdefault("parent", maya_window)
    kwargs.setdefault("tearOff", True)

    name = label.replace("_", " ")  # maya menu names can't have underscores

    return maya.cmds.menu(name, **kwargs)


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

            self.name = self.label
            return maya.cmds.menuItem(self.name, **kwargs)

    def _setup_menu_item(self, parent_app_node=None):
        icon = self.icon or ""
        tooltip = self.tooltip or "test"

        # support adding custom kwargs from the config
        kwargs = self.kwargs
        kwargs.setdefault("label", self.label)
        kwargs.setdefault("command", self.run)
        kwargs.setdefault("parent", parent_app_node)
        kwargs.setdefault("image", icon)
        kwargs.setdefault("annotation", tooltip)  # shown on hover in lower left corner

        self.name = self.label

        return maya.cmds.menuItem(self.name, **kwargs)

    def _setup_separator(self, parent_app_node=None):
        self.name = self.label

        # support adding custom kwargs from the config
        kwargs = self.kwargs
        kwargs.setdefault("divider", True)
        kwargs.setdefault("dividerLabel", self.label)
        kwargs.setdefault("parent", parent_app_node)

        return maya.cmds.menuItem(self.name, **kwargs)

    def teardown(self):
        # see https://stackoverflow.com/questions/44142119/remove-menu-item-in-maya-using-python
        # todo can we remove self.name? bit hacky
        maya.cmds.deleteUI(self.name, menu=True)

