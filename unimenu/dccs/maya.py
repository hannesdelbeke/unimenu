import pymel.core as pm  # todo replace with cmds because it's faster
from unimenu.dccs._abstract import AbstractMenuMaker


class MenuMaker(AbstractMenuMaker):
    @classmethod
    def setup_menu(cls, data) -> pm.menu:
        label = data.get("label")  # root menu name
        parent = data.get("parent")  # todo parent

        # todo parent logic currently is re implemented in every dcc module
        #  can we move it to the abstract class?
        # if we provide a parent in the config, we might want to parent to a submenu


        menu = cls.create_root_menu(label)
        cls._setup_menu_items(menu, data.get("items"))
        return menu

    @classmethod
    def create_root_menu(cls, label, window_name=None):
        """
        Create a root menu in Maya
        label: str, the label of the menu
        window_name: str, the name of the window to attach the menu to
        """
        window_name = window_name or "gMainWindow"  # default value

        maya_window = pm.language.melGlobals[window_name]
        return pm.menu(label, parent=maya_window, tearOff=True)

    @classmethod
    def add_sub_menu(cls, parent, label: str):
        return pm.menuItem(subMenu=True, label=label, parent=parent, tearOff=True)

    @classmethod
    def add_to_menu(cls, parent, label: str, command: str, icon: str = None, tooltip: str = None):
        icon = icon or ""
        tooltip = tooltip or ""

        return pm.menuItem(label=label, command=command, parent=parent, image=icon)
        # todo menuItem doesn't support tooltip.
        #  could use qt instead http://discourse.techart.online/t/is-there-a-way-to-get-tooltips-for-maya-menitem/15385

    @classmethod
    def teardown_menu(cls, name: str):
        """remove from menu"""
        # see https://stackoverflow.com/questions/44142119/remove-menu-item-in-maya-using-python
        pm.deleteUI(name, menu=True)

    @classmethod
    def add_separator(cls, parent, label: str = None):
        return pm.menuItem(divider=True, parent=parent, dividerLabel=label)


setup_menu = MenuMaker.setup_menu
teardown_menu = MenuMaker.teardown_menu
