"""
generate menus in 3ds max

generated menus are persistent between sessions!
"""

from pymxs import runtime as rt
from pathlib import Path

from unimenu.dccs._abstract import AbstractMenuMaker


counter = -1


class MenuMaker(AbstractMenuMaker):
    @classmethod
    def setup_menu(cls, data):
        mainMenuBar = rt.menuMan.getMainMenuBar()
        cls._setup_menu_items(mainMenuBar, data.get("items"))
        rt.menuMan.updateMenuBar()

    # @classmethod
    # def _setup_menu_items(cls, parent, items: list):
    #     """
    #     recursively add all menu items and submenus
    #     """
    #     for item in items:
    #
    #         # check if item is not a divider
    #         if item == "---":  # todo add divider support to all other dccs
    #             cls.add_separator(parent)
    #             continue
    #
    #         label = item.get("label")
    #         tooltip = item.get("tooltip")
    #         command = item.get("command", None)
    #         if command:
    #             cls.add_to_menu(parent, label, command, tooltip)
    #         else:  # submenu
    #             items = item.get("items", [])
    #             sub_menu = cls.add_sub_menu(parent, label)
    #             cls._setup_menu_items(sub_menu, items)

    @classmethod
    def add_sub_menu(cls, parent, label):
        sub_menu = rt.menuMan.createMenu(label)
        sub_menu_item = rt.menuMan.createSubMenuItem(label, sub_menu)
        parent.addItem(sub_menu_item, -1)
        return sub_menu

    @classmethod
    def add_to_menu(cls, parent, label: str, command: str, tooltip: str = None):

        tooltip = tooltip or ""

        # todo generated menus are persistent between sessions!
        #  this does not match the behavior of other DCCs currently
        #  a macro is created at C:\Users\hanne\AppData\Local\Autodesk\3dsMax\2024 - 64bit\ENU\usermacros\
        macro_name, macro_category = cls.create_macro(label, command)
        # todo handle case when we create a macro with the same name as an existing macro
        # since actionitems are based of macro names, we can't have two actionitems with the same name
        item = rt.menuMan.createActionItem(macro_name, macro_category)
        parent.addItem(item, -1)  # item index

    @classmethod
    def add_separator(cls, parent):
        item = rt.menuMan.createSeparatorItem()
        parent.addItem(item, -1)  # item index

    @classmethod
    def add_callable_to_maxscript(cls, command):
        """
        add to runtime, creating a callable var in maxscript
        command: (str or callable) execute string as python code, or run callable
        """
        global counter  # counter guarantees unique macro names
        counter += 1

        def _execute_command():
            if isinstance(command, str):
                exec(command)
            else:
                command()

        cmd_name = f"unimenu_{counter}"
        setattr(rt, cmd_name, _execute_command)  # add to runtime, creating a callable var in maxscript

        return cmd_name

    @classmethod
    def create_macro(cls, label, command):
        """
        create a macroscript exposed to maxscript
        """
        cmd_name = cls.add_callable_to_maxscript(command)

        macro_name = cmd_name
        macro_category = "UniMenu"
        macro_tooltip = "This is a tooltip"  # TODO this doesn't work
        macro_text = label
        macro_content = cmd_name + "()"
        macro_id = rt.macros.new(macro_category, macro_name, macro_tooltip, macro_text, macro_content)
        return macro_name, macro_category

    @classmethod
    def teardown(cls):
        """remove from menu"""

        # todo remove dynamically created macros
        macros_path = Path(rt.pathConfig.getDir(rt.name("Additional Macros")))
        # delete all files containing unimenu in their name, in the folder with path macros_path
        for file in macros_path.glob("unimenu*"):
            file.unlink()

        # get info from macros and remove from menu
        # track submenus created, across sessions

        raise NotImplementedError("not yet implemented")

    @classmethod
    def teardown_by_name(cls, name):
        # todo since this is based on remove menu by name, ensure we don't remove default max menus.
        #  use some kind of unimenu append to name on creation
        #  also handle duplicate names
        menu_interface = rt.menuMan.findMenu(name)
        rt.menuMan.unRegisterMenu(menu_interface)


# menu man pymxs official https://help.autodesk.com/view/MAXDEV/2022/ENU/?guid=Max_Python_API_using_pymxs_pymxs_macroscripts_menus_html
# maxscript menuman ref https://help.autodesk.com/view/3DSMAX/2017/ENU/?guid=__files_GUID_258F6015_6B45_4A87_A7F5_BB091A2AE065_htm


setup_menu = MenuMaker.setup_menu
