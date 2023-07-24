import logging
from unimenu.apps._abstract import MenuNodeAbstract
import nuke


class MenuNodeNuke(MenuNodeAbstract):
    nuke_menu_instance = ["Nuke", "Pane", "Nodes", "Properties", "Animation", "Viewer", "Node Graph", "Axis"]

    @property
    def _default_root_parent(self):
        if self.parent_path:
            parent_path = self.parent_path if self.parent_path in self.nuke_menu_instance else "Nuke"
        else:
            parent_path = self.nuke_menu_instance[0]
        menubar = nuke.menu(parent_path)
        return menubar

    def _setup_sub_menu(self, parent_app_node=None):

        if not self.label:  # todo move to abstract node
            self.label = "custom_menu"

        parent_app_node = parent_app_node or nuke.menu("Nuke")
        if self.icon:
            return parent_app_node.addMenu(self.label, self.icon, **self.kwargs)
        else:
            return parent_app_node.addMenu(self.label, **self.kwargs)

    def _setup_menu_item(self, parent_app_node=None):
        parent_app_node.addCommand(self.label, self.run, **self.kwargs)

    def _setup_separator(self, parent_app_node=None):
        if parent_app_node:
            parent_app_node.addSeparator(**self.kwargs)

    def teardown(self):
        menubar = nuke.menu(self.parent_path)
        menu = menubar.findItem(self.name)
        for item in menu.items():
            logging.info("Removing menu item: {}".format(item.name()))
            menu.removeItem(item.name())
