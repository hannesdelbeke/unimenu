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


def create_root_menu(label, window_name=None) -> pm.menu:
    """
    Create a root menu in Maya
    label: str, the label of the menu
    window_name: str, the name of the window to attach the menu to
    """
    window_name = window_name or "gMainWindow"  # default value

    maya_window = pm.language.melGlobals[window_name]
    return pm.menu(label, parent=maya_window, tearOff=True)  # todo garantuee unique name


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
            menu = create_root_menu(self.label)
        return menu

    def _setup_sub_menu(self, parent_app_node=None):
        # todo handle uniqyue name, atm label can clash with other menu items

        self.counter += 1
        self.name = f"{self.label}_{self.counter}"

        return pm.menuItem(self.name, subMenu=True, label=self.label, parent=parent_app_node, tearOff=True)


    def _setup_menu_item(self, parent_app_node=None):
        icon = self.icon or ""
        tooltip = self.tooltip or ""

        self.counter += 1
        self.name = f"{self.label}_{self.counter}"

        return pm.menuItem(self.name, label=self.label, command=self.command, parent=parent_app_node, image=icon)
        # todo menuItem doesn't support tooltip.
        #  could use qt instead http://discourse.techart.online/t/is-there-a-way-to-get-tooltips-for-maya-menitem/15385


    def _setup_separator(self, parent_app_node=None):
        self.counter += 1
        self.name = f"{self.label}_{self.counter}"

        return pm.menuItem(self.name, divider=True, parent=parent_app_node, dividerLabel=self.label)

    def teardown(self):
        # see https://stackoverflow.com/questions/44142119/remove-menu-item-in-maya-using-python
        # todo can we remove self.name? bit hacky
        pm.deleteUI(self.name, menu=True)
