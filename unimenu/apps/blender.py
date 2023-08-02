"""
# 1. load data
# 2. create operators (classes)
# 3. register operators
# 4. add operators to menu
"""
import logging
import pathlib

import bpy
import bpy.utils.previews
from typing import Union, Callable
from unimenu.apps._abstract import MenuNodeAbstract
import unimenu.apps


preview_collections = {}  # store custom icons here to prevent blender warnings
# todo cleanup on teardown / unload with bpy.utils.previews.remove(preview_collection)


def unique_operator_name(name) -> str:
    """ensure unique name for blender operators, adds _number to the end if name not unique"""
    unique_counter = 1  # start count from 2
    new_name = name
    while new_name in dir(bpy.types):
        unique_counter += 1
        new_name = f"{name}_{unique_counter}"
    return new_name


def create_custom_icon(path, name: str = None):
    """
    helper method to create a custom icon

    path: path to png

    returns icon ID
    """
    name = name or "icon_name"

    preview_collection = preview_collections.get(path)
    if preview_collection:
        return preview_collection[name].icon_id

    preview_collection = bpy.utils.previews.new()
    preview_collections[path] = preview_collection
    icon = preview_collection.load(name=name, path=str(path), path_type='IMAGE')
    icon_ID = icon.icon_id

    return icon_ID


def operator_wrapper(
    parent: bpy.types.Operator, label: str, id: str, command: Union[str, Callable], icon=None, tooltip=None
) -> bpy.types.Operator:
    """
    Wrap a command in a Blender operator & add it to a parent menu operator.

    1 make class
    2 register class
    3 add to (sub)menu (parent operator)
    """

    icon = icon or "NONE"
    tooltip = tooltip or ""

    # handle name
    # class: UNIMENU_OT_my_operator
    # id: unimenu.my_operator
    #  todo add support dupe names
    name = "UNIMENU_OT_" + id
    name = unique_operator_name(name)
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
            self._command()
            return {"FINISHED"}

    # print("UNI made operator", name, OperatorWrapper.bl_idname)
    OperatorWrapper.__name__ = name
    if tooltip:
        OperatorWrapper.__doc__ = tooltip

    # register
    bpy.utils.register_class(OperatorWrapper)

    # ensure None was not accidentally passed
    icon = icon or "NONE"

    # add to menu
    def menu_draw(self, context):  # self is the parent menu
        _icon_ID = None
        _icon_name = None

        if isinstance(icon, int):  # use icon ID for custom icons
            logging.debug(f"icon is int: {icon}")
            _icon_ID = icon

        elif isinstance(icon, str):  # if str, can be default icon name, or a string path
            logging.debug(f"icon is str: {icon}")

            # check if it's a path
            if pathlib.Path(icon).exists():
                logging.debug(f"icon str path exists: {icon}")
                _icon_ID = create_custom_icon(icon)

            else:  # assume icon is a default icon name
                logging.debug(f"icon str path doesn't exists: {icon}, assuming it's a default icon name")
                _icon_name=icon

        elif isinstance(icon, pathlib.Path):  # use icon path for custom icons
            _icon_ID = create_custom_icon(icon)

        else:
            raise TypeError(f"icon '{icon}' isn't a valid type '{type(icon)}', "
                            f"expecting str, int, Path")

        if _icon_name:
            self.layout.operator(id_name, icon=_icon_name)
        elif _icon_ID:
            self.layout.operator(id_name, icon_value=_icon_ID)
        else:
            self.layout.operator(id_name, icon="NONE")


    def try_menu_draw(self, context):  # self is the parent menu
        # todo check if icon exists, if not use NONE, for now dirty try except hack
        try:
            return menu_draw(self, context)
        except TypeError:  # icon not found:
            return self.layout.operator(id_name, icon="NONE")

    parent.append(try_menu_draw)

    return OperatorWrapper



def menu_wrapper(parent: bpy.types.Operator, label: str) -> bpy.types.Menu:
    """
    1 make class
    2 register class
    3 add to (sub)menu (parent operator)
    """

    # global counter
    # counter += 1
    # todo add support dupe names
    # handle name
    # class: UNIMENU_OT_my_operator
    # id: unimenu.my_operator
    # todo we dont need to set both class and bl_idname

    name = "UNIMENU_MT_" + label.replace(" ", "_")

    name = unique_operator_name(name)

    id_name = name

    class MenuWrapper(bpy.types.Menu):
        bl_label = label
        bl_idname = id_name

        def draw(self, context):
            layout = self.layout  # layout is needed, even when unused

    # rename class
    MenuWrapper.__name__ = name
    # print("UNI made menu operator", name, MenuWrapper.bl_idname)

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
        if self.parent_path:
            parent_path = f"UNIMENU_MT_{self.parent_path.replace(' ', '_')}"
        else:
            parent_path = "TOPBAR_MT_editor_menus"
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
        return operator_wrapper(parent=parent_app_node, label=self.label, id=self.id, command=self.run, icon=icon, tooltip=tooltip)

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

