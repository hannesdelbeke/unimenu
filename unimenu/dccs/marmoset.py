"""
marmoset doesn't support menu extensions,
so we create windows with buttons instead, submenus create new windows
"""

import mset
from unimenu.dccs._abstract import AbstractMenuMaker, MenuNodeAbstract


windows = []


class MenuMaker(AbstractMenuMaker):
    @classmethod
    def setup_menu(cls, data):
        cls._setup_menu_items(None, data.get("items"))

    @classmethod
    def add_sub_menu(cls, parent, label: str):
        global windows
        if not parent:
            window = mset.UIWindow(label)
            # save window in a global to prevent garbage collection
            windows.append(window)
            return window

        settings_drawer_ui = mset.UIDrawer(name=label)
        settings_drawer = mset.UIWindow(name="", register=False)
        settings_drawer_ui.containedControl = settings_drawer

        parent.addReturn()  # work vertically since else window looks bad
        parent.addElement(settings_drawer_ui)
        parent.addReturn()

        return settings_drawer

    @classmethod
    def add_to_menu(cls, parent, label: str, command: str):
        def cmd():
            if isinstance(command, str):
                exec(command)
            else:
                command()

        button = mset.UIButton()
        button.text = label
        button.onClick = cmd
        parent.addElement(button)
        return button

    @classmethod
    def teardown_menu(cls):
        """remove from menu"""
        raise NotImplementedError("not yet implemented")


setup_menu = MenuMaker.setup_menu


class MenuNode(MenuNodeAbstract):
    # @property
    # def _default_root_parent(self):

    def _setup_sub_menu(self, parent_app_node=None):
        return MenuMaker.add_sub_menu(parent=parent_app_node, label=self.label)

    def _setup_menu_item(self, parent_app_node=None):
        return MenuMaker.add_to_menu(parent=parent_app_node, label=self.label, command=self.command)

    def _setup_separator(self, parent_app_node=None):
        return MenuMaker.add_separator(parent=parent_app_node, label=self.label)

    def teardown(self):
        return MenuMaker.teardown_menu()
