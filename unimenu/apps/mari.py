from unimenu.apps._abstract import MenuNodeAbstract
import mari


class MenuNodeMari(MenuNodeAbstract):

    def setup(self, parent_app_node=None, backlink=False):
        super().setup(parent_app_node=parent_app_node, backlink=backlink)

    @property
    def _default_root_parent(self):
        return "MainWindow"

    def _setup_sub_menu(self, parent_app_node=None):
        if parent_app_node:
            return f"{parent_app_node}/{self.label}"
        return "MainWindow"

    def _setup_menu_item(self, parent_app_node=None):
        if parent_app_node:
            action = mari.actions.create(self.label, self.run)
            mari.menus.addAction(action, parent_app_node)

    def _setup_separator(self, parent_app_node=None):
        if parent_app_node:
            mari.menus.addSeparator(parent_app_node)

    def teardown(self):
        """remove from menu"""
        pass
