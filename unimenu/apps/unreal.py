import unreal
from unimenu.apps._abstract import MenuNodeAbstract
import logging


class MenuNodeUnreal(MenuNodeAbstract):

    @property
    def _default_root_parent(self):
        if not self.parent_path:
            self.parent_path = "LevelEditor.MainMenu"

        unreal_menus = unreal.ToolMenus.get()
        parent_menu = unreal_menus.find_menu(self.parent_path)
        return parent_menu

    def setup(self, parent_app_node=None, backlink=True):
        # save  section name to data before setup
        user_section = self.kwargs.get('menu_section')
        self.data['target_section_name'] = user_section if user_section else "PythonTools"

        super().setup(parent_app_node=parent_app_node, backlink=backlink)

        # post setup
        unreal_menus = unreal.ToolMenus.get()
        unreal_menus.refresh_all_widgets()

    def _setup_sub_menu(self, parent_app_node=None) -> unreal.ToolMenu:
        if not self.check_unique_name():
            raise Exception(f"Menu '{self.label}' already exists, stopping submenu setup")

        return parent_app_node.add_sub_menu(
            owner=parent_app_node.menu_name,
            section_name=self.data['target_section_name'],
            name=self.id,  # todo check if needs to be unique like in add_to_menu
            label=self.label,  # todo add label support
            tool_tip=self.tooltip
        )

    def _setup_menu_item(self, parent_app_node=None) -> unreal.ToolMenuEntry:
        """add a menu item to the script menu"""
        if not self.check_unique_name():
            raise Exception(f"Menu item '{self.label}' already exists, stopping menu item setup")

        entry = unreal.ToolMenuEntry(
            name=self.id,  # this needs to be unique! if not set, it's autogenerated
            type=unreal.MultiBlockType.MENU_ENTRY,
            insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.FIRST),
        )
        if self.label:
            entry.set_label(self.label)
        if self.command:
            entry.set_string_command(
                type=unreal.ToolMenuStringCommandType.PYTHON,
                string=self.command,
                custom_type=unreal.Name("_placeholder_"),
            )  # hack: unsure what custom_type does, but it's needed
        if self.tooltip:
            entry.set_tool_tip(self.tooltip)
        if self.icon:
            entry.set_icon(self.icon)  # naive implementation todo improve

        parent_app_node.add_menu_entry(self.data['target_section_name'], entry)  # always returns None
        return entry

    def _setup_separator(self, parent_app_node=None):
        # todo not working yet
        """add a separator to the script menu"""
        # see https://docs.unrealengine.com/4.27/en-US/PythonAPI/class/ToolMenu.html
        # todo what is diff with dynamic section?
        return parent_app_node.add_section(section_name=self.label + "_section", label=self.label + "_label")

    def teardown(self):
        """remove from menu"""
        raise NotImplementedError("not yet implemented")

    def check_unique_name(self):
        """check if menu exists already, return True if it does not exist"""
        # unreal_menus.find_menu("LevelEditor.MainMenu.Tools")
        unreal_menus = unreal.ToolMenus.get()
        #
        exists = unreal_menus.find_menu(self.get_name_path())
        if exists:
            logging.warning(f"Menu already exists: '{self.get_name_path()}'")
            parent_label = self.parent.label if self.parent else None
            logging.warning(f"Parent is '{parent_label}'")
            return False
        else:
            return True

    def get_name_path(self):
        # e.g. return 'LevelEditor.MainMenu.Tools' if self.id is 'Tools'
        if self.parent:
            return self.parent.get_parent_path() + "." + self.id
        else:
            return self.parent_path + "." + self.id