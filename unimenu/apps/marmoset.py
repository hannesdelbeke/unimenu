"""
marmoset doesn't support menu extensions,
so we create windows with buttons instead, submenus create new windows
"""

import mset
from unimenu.apps._abstract import MenuNodeAbstract


windows = []


class MenuNodeMarmoset(MenuNodeAbstract):
    # @property
    # def _default_root_parent(self):

    def _setup_sub_menu(self, parent_app_node=None):

        global windows
        if not parent_app_node:
            window = mset.UIWindow(self.label)
            # save window in a global to prevent garbage collection
            windows.append(window)
            return window

        settings_drawer_ui = mset.UIDrawer(name=self.label)
        settings_drawer = mset.UIWindow(name="", register=False)
        settings_drawer_ui.containedControl = settings_drawer

        parent_app_node.addReturn()  # work vertically since else window looks bad
        parent_app_node.addElement(settings_drawer_ui)
        parent_app_node.addReturn()

        return settings_drawer

    def _setup_menu_item(self, parent_app_node=None):

        def cmd():
            if isinstance(self.command, str):
                exec(self.command)
            else:
                self.command()

        button = mset.UIButton()
        button.text = self.label
        button.onClick = cmd
        parent_app_node.addElement(button)
        return button

    def _setup_separator(self, parent_app_node=None):
        raise NotImplementedError("not yet implemented")

    def teardown(self):
        """remove from menu"""
        raise NotImplementedError("not yet implemented")
