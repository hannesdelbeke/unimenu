"""
generate menus in 3ds max

generated menus with menuMan are persistent between sessions!
recommended to use qt instead, to generate menus on startup
"""

from pymxs import runtime as rt
from unimenu.apps._abstract import MenuNodeAbstract


# menu man pymxs official https://help.autodesk.com/view/MAXDEV/2022/ENU/?guid=Max_Python_API_using_pymxs_pymxs_macroscripts_menus_html
# maxscript menuman ref https://help.autodesk.com/view/3DSMAX/2017/ENU/?guid=__files_GUID_258F6015_6B45_4A87_A7F5_BB091A2AE065_htm


class MenuNodeMax(MenuNodeAbstract):

    def setup(self, parent_app_node=None, backlink=True):
        super().setup(parent_app_node=parent_app_node, backlink=backlink)
        rt.menuMan.updateMenuBar()

    @property
    def _default_root_parent(self):
        return rt.menuMan.getMainMenuBar()

    def _setup_sub_menu(self, parent_app_node=None):
        sub_menu = rt.menuMan.createMenu(self.label)
        sub_menu_item = rt.menuMan.createSubMenuItem(self.label, sub_menu)
        parent_app_node.addItem(sub_menu_item, -1)
        return sub_menu

    def _setup_menu_item(self, parent_app_node=None):
        tooltip = self.tooltip or ""

        # todo generated menus are persistent between sessions!
        #  this does not match the behavior of other Apps currently
        #  a macro is created at C:\Users\hanne\AppData\Local\Autodesk\3dsMax\2024 - 64bit\ENU\usermacros\
        macro_name, macro_category = create_macro(self.label, self.command)
        # todo handle case when we create a macro with the same name as an existing macro
        # since actionitems are based of macro names, we can't have two actionitems with the same name
        item = rt.menuMan.createActionItem(macro_name, macro_category)
        parent_app_node.addItem(item, -1)  # item index

    def _setup_separator(self, parent_app_node=None):
        item = rt.menuMan.createSeparatorItem()
        parent_app_node.addItem(item, -1)  # item index

    def teardown(self):
        pass

    # def teardown(cls):
    #     """remove from menu"""
    #
    #     # todo remove dynamically created macros
    #     macros_path = Path(rt.pathConfig.getDir(rt.name("Additional Macros")))
    #     # delete all files containing unimenu in their name, in the folder with path macros_path
    #     for file in macros_path.glob("unimenu*"):
    #         file.unlink()
    #
    #     # get info from macros and remove from menu
    #     # track submenus created, across sessions
    #
    #     raise NotImplementedError("not yet implemented")
    #
    # def teardown_by_name(cls, name):
    #     # todo since this is based on remove menu by name, ensure we don't remove default max menus.
    #     #  use some kind of unimenu append to name on creation
    #     #  also handle duplicate names
    #     menu_interface = rt.menuMan.findMenu(name)
    #     rt.menuMan.unRegisterMenu(menu_interface)


counter = -1


# todo bit hacky can this be cleaner?
def add_callable_to_maxscript(command):
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


def create_macro(label, command):
    """
    create a macroscript exposed to maxscript
    """
    cmd_name = add_callable_to_maxscript(command)

    macro_name = cmd_name
    macro_category = "UniMenu"
    macro_tooltip = "This is a tooltip"  # TODO this doesn't work
    macro_text = label
    macro_content = cmd_name + "()"
    macro_id = rt.macros.new(macro_category, macro_name, macro_tooltip, macro_text, macro_content)
    return macro_name, macro_category