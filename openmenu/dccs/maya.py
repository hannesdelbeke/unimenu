import pymel.core as pm  # todo replace with cmds because it's faster


from openmenu.dccs._abstract import AbstractMenuMaker


class MenuMaker(AbstractMenuMaker):

    @classmethod
    def setup_menu(cls, data):
        menu = cls.create_root_menu("OpenMenu")
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
    def add_to_menu(cls, parent, label: str, command: str, icon: str = "", tooltip: str = ""):
        # menuItem doesn't support tooltip.
        # could use qt instead http://discourse.techart.online/t/is-there-a-way-to-get-tooltips-for-maya-menitem/15385
        return pm.menuItem(label=label, command=command, parent=parent, image=icon)

    @classmethod
    def teardown_menu(cls):
        """remove from menu"""
        raise NotImplementedError("not yet implemented")

setup_menu = MenuMaker.setup_menu