import pymel.core as pm  # todo replace with cmds because it's faster


from unimenu.dccs._abstract import AbstractMenuMaker


class MenuMaker(AbstractMenuMaker):
    @classmethod
    def setup_menu(cls, data):
        menu = cls.create_root_menu("UniMenu")
        cls._setup_menu_items(menu, data.get("items"))

    @classmethod
    def create_root_menu(cls, label, window_name="gMainWindow"):
        """
        Create a root menu in Maya
        label: str, the label of the menu
        window_name: str, the name of the window to attach the menu to
        """
        maya_window = pm.language.melGlobals[window_name]
        return pm.menu(label, parent=maya_window)

    @classmethod
    def add_sub_menu(cls, parent, label: str):
        return pm.menuItem(subMenu=True, label=label, parent=parent)

    # https://help.autodesk.com/cloudhelp/2018/JPN/Maya-Tech-Docs/PyMel/generated/functions/pymel.core.windows/pymel.core.windows.menuItem.html
    @classmethod
    def add_to_menu(cls, parent, label: str, command: str, icon: str = None, tooltip: str = None):
        # default kwarg values set here, since when set in the function signature we get bugs.
        icon = icon or ""
        tooltip = tooltip or ""

        # menuItem doesn't support tooltip.
        # could use qt instead http://discourse.techart.online/t/is-there-a-way-to-get-tooltips-for-maya-menitem/15385
        return pm.menuItem(label=label, command=command, parent=parent, image=icon)

    @classmethod
    def teardown_menu(cls):
        """remove from menu"""
        raise NotImplementedError("not yet implemented")

    @classmethod
    def add_separator(cls, parent):
        return pm.menuItem(divider=True, parent=parent)


setup_menu = MenuMaker.setup_menu
