import pymel.core as pm  # todo replace with cmds because it's faster
from unimenu.dccs._abstract import MenuNodeAbstract
import maya.mel
import maya.cmds


def find_menu(name):
    gMainWindow = maya.mel.eval('$temp=$gMainWindow')
    # get all the menus that are children of the main menu
    mainWindowMenus = maya.cmds.window(gMainWindow, query=True, menuArray=True)
    for menu in mainWindowMenus:
        print(menu)
        if menu.lower() == name.lower():
            return menu

        # TODO get their children recursively


def create_root_menu(label, window_name=None, kwargs=None, counter=0) -> pm.menu:
    """
    Create a root menu in Maya
    label: str, the label of the menu
    window_name: str, the name of the window to attach the menu to
    """
    window_name = window_name or "gMainWindow"  # default value
    maya_window = pm.language.melGlobals[window_name]

    kwargs = {"parent": maya_window, "tearOff": True}
    kwargs |= kwargs  # support adding custom kwargs from the config

    name = f"{label}_{counter}"

    return pm.menu(name, **kwargs)


class MenuNodeMaya(MenuNodeAbstract):
    counter = 0

    @property
    def _default_root_parent(self):

        # todo parent logic currently is re implemented in every dcc module
        #  can we move it to the abstract class?
        # if we provide a parent in the config, we might want to parent to a submenu
        if self.parent_path:
            menu = find_menu(self.parent_path)
        else:
            menu = create_root_menu(self.label, kwargs=self.kwargs, counter=self.counter)
        return menu

    def _setup_sub_menu(self, parent_app_node=None):
        # todo handle unique name, atm label can clash with other menu items

        self.counter += 1
        self.name = f"{self.label}_{self.counter}"

        kwargs = {"subMenu": True, "label": self.label, "parent": parent_app_node, "tearOff": True}
        kwargs |= self.kwargs  # support adding custom kwargs from the config
        return pm.menuItem(self.name, **kwargs)

    def _setup_menu_item(self, parent_app_node=None):
        icon = self.icon or ""

        # tooltip = self.tooltip or ""
        # todo menuItem doesn't support tooltip.
        #  could use qt instead http://discourse.techart.online/t/is-there-a-way-to-get-tooltips-for-maya-menitem/15385

        kwargs = {"label": self.label, "command": self.command, "parent": parent_app_node, "image": icon}
        kwargs |= self.kwargs  # support adding custom kwargs from the config

        self.counter += 1
        self.name = f"{self.label}_{self.counter}"

        return pm.menuItem(self.name, **kwargs)

    def _setup_separator(self, parent_app_node=None):
        self.counter += 1
        self.name = f"{self.label}_{self.counter}"

        kwargs = {"divider": True, "dividerLabel": self.label, "parent": parent_app_node}
        kwargs |= self.kwargs  # support adding custom kwargs from the config

        return pm.menuItem(self.name, **kwargs)

    def teardown(self):
        # see https://stackoverflow.com/questions/44142119/remove-menu-item-in-maya-using-python
        # todo can we remove self.name? bit hacky
        pm.deleteUI(self.name, menu=True)
