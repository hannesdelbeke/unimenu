"""
# 1. load data
# 2. create operators (classes)
# 3. register operators
# 4. add operators to menu
"""
import bpy
from typing import Union, Callable
from openmenu.dccs._abstract import AbstractMenuMaker


class MenuMaker(AbstractMenuMaker):
    registered_operators = set()

    @classmethod
    def setup_menu(cls, data):
        """
        setup menu from data
        return all created operators
        """
        # global registered_operators

        # get data
        items = data.get("items")
        parent_name = data.get("parent_menu") or "TOPBAR_MT_editor_menus"
        parent = getattr(bpy.types, parent_name)

        operators = cls._setup_menu_items(parent, items)
        cls.registered_operators.update(operators)
        return operators

    @classmethod
    def teardown_menu(cls, data):  # operators=None, parent_name="TOPBAR_MT_editor_menus"):
        """
        remove from menu
        if no operators are passed, remove all operators
        """

        # todo add support for data, atm removes everything

        # global registered_operators
        # operators = operators or registered_operators
        for op in cls.registered_operators:
            bpy.utils.unregister_class(op)

        # # add root menu to menu
        # parent = getattr(bpy.types, parent_name)
        # parent.remove(draw_menu)  # TODO somehow track draw_menu callable

    @classmethod
    def add_sub_menu(cls, parent: bpy.types.Operator, label: str):
        return menu_wrapper(parent, label)

    @classmethod
    def add_to_menu(cls, parent: bpy.types.Operator, label: str, command: str, icon="NONE", tooltip=""):
        return operator_wrapper(parent, label, command, icon_name=icon, tooltip=tooltip)

    @classmethod
    def add_separator(cls, parent: bpy.types.Operator):
        parent.append(lambda self, context: self.layout.separator())


def operator_wrapper(
    parent: bpy.types.Operator, label: str, command: Union[str, Callable], icon_name="NONE", tooltip=""
):
    """
    Wrap a command in a Blender operator & add it to a parent menu operator.

    1 make class
    2 register class
    3 add to (sub)menu (parent operator)
    """

    # handle name
    # class: OPENMENU_OT_my_operator
    # id: openmenu.my_operator
    #  todo add support dupe names
    name = "OPENMENU_OT_" + label.replace(" ", "_")
    id_name = name.replace("OPENMENU_OT_", "openmenu.").lower()

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


def menu_wrapper(parent: bpy.types.Operator, label: str):
    """
    1 make class
    2 register class
    3 add to (sub)menu (parent operator)
    """

    # todo add support dupe names
    # handle name
    # class: OPENMENU_OT_my_operator
    # id: openmenu.my_operator
    # todo we dont need to set both class and bl_idname

    name = "OPENMENU_MT_" + label.replace(" ", "_")
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

    parent.append(menu_draw)

    return MenuWrapper


setup_menu = MenuMaker.setup_menu
