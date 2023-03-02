"""
# 1. load data
# 2. create operators (classes)
# 3. register operators
# 4. add operators to menu
"""
import bpy
from typing import Union, Callable
from unimenu.apps._abstract import MenuNodeAbstract
import unimenu.apps


counter = -1

def operator_wrapper(
    parent: bpy.types.Operator, label: str, command: Union[str, Callable], icon_name=None, tooltip=None
) -> bpy.types.Operator:
    """
    Wrap a command in a Blender operator & add it to a parent menu operator.

    1 make class
    2 register class
    3 add to (sub)menu (parent operator)
    """

    global counter
    counter += 1

    icon_name = icon_name or "NONE"
    tooltip = tooltip or ""

    # handle name
    # class: UNIMENU_OT_my_operator
    # id: unimenu.my_operator
    #  todo add support dupe names
    name = "UNIMENU_OT_" + label.replace(" ", "_") + str(counter)
    id_name = name.replace("UNIMENU_OT_", "unimenu.").lower()

    # create
    class OperatorWrapper(bpy.types.Operator):
        # blender vars
        bl_label = label
        bl_idname = id_name

        # custom vars
        _command = command  # custom var to store string command
        _parent_name = parent.bl_idname

        def execute(self, context):
            # data loaded from the config passes strings to eval,
            # but dynamically created configs support callables

            if isinstance(self._command, str):
                exec(self._command)

            elif callable(self._command):
                self._command()

            return {"RUNNING_MODAL"}

    OperatorWrapper.__name__ = name
    if tooltip:
        OperatorWrapper.__doc__ = tooltip

    # register
    bpy.utils.register_class(OperatorWrapper)

    # ensure None was not accidentally passed
    icon_name = icon_name or "NONE"

    # add to menu
    def menu_draw(self, context):  # self is the parent menu
        self.layout.operator(id_name, icon=icon_name)

    parent.append(menu_draw)

    return OperatorWrapper


def menu_wrapper(parent: bpy.types.Operator, label: str) -> bpy.types.Menu:
    """
    1 make class
    2 register class
    3 add to (sub)menu (parent operator)
    """

    global counter
    counter += 1
    # todo add support dupe names
    # handle name
    # class: UNIMENU_OT_my_operator
    # id: unimenu.my_operator
    # todo we dont need to set both class and bl_idname

    name = "UNIMENU_MT_" + label.replace(" ", "_") + str(counter)
    id_name = name

    class MenuWrapper(bpy.types.Menu):
        bl_label = label
        bl_idname = id_name

        def draw(self, context):
            layout = self.layout  # layout is needed, even when unused

    # rename class
    MenuWrapper.__name__ = name

    # register
    bpy.utils.register_class(MenuWrapper)

    # add to menu
    def menu_draw(self, context):  # self is the parent menu
        self.layout.menu(id_name)
        # TODO fix bug in above line
        #  search for unknown menutype UNIMENU_MT_UniMenu3
        #  uiItemM: not found UNIMENU_MT_UniMenu3

    parent.append(menu_draw)

    return MenuWrapper


class MenuNodeBlender(MenuNodeAbstract):
    app = unimenu.apps.SupportedApps.BLENDER  # helper to get matching App

    @property
    def _default_root_parent(self):
        parent_path = self.parent_path or "TOPBAR_MT_editor_menus"
        parent_node = getattr(bpy.types, parent_path)  # get the parent from blender by name
        return parent_node

        # # create app menu-nodes
        # operators = cls._setup_menu_items(parent, items=menu_node.items)
        # cls.registered_operators.update(operators)
        # return operators

    def _setup_sub_menu(self, parent_app_node=None) -> bpy.types.Menu:
        return menu_wrapper(parent=parent_app_node, label=self.label)

    def _setup_menu_item(self, parent_app_node=None) -> bpy.types.Operator:
        icon = self.icon or "NONE"
        tooltip = self.tooltip or ""
        return operator_wrapper(parent_app_node, self.label, self.command, icon_name=icon, tooltip=tooltip)

    def _setup_separator(self, parent_app_node=None):
        # todo return separator correctly
        parent_app_node.append(lambda self, context: self.layout.separator())

    def teardown(self):
        """
        remove from menu
        if no operators are passed, remove all operators
        """
        if self.items:
            for item in self.items:
                item.teardown()

        operator = self.app_node
        if operator:
            print("teardown", operator.bl_idname)
            bpy.utils.unregister_class(operator)

        # # add root menu to menu
        # parent = getattr(bpy.types, parent_name)
        # parent.remove(draw_menu)  # TODO somehow track draw_menu callable

