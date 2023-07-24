from unimenu.apps._abstract import MenuNodeAbstract
from UI4.App import MainWindow


class MenuNodeKatana(MenuNodeAbstract):

    @property
    def _default_root_parent(self):
        menu_bar = MainWindow.GetMainWindow().getMenuBar()
        return menu_bar

    def _setup_sub_menu(self, parent_app_node=None):
        if parent_app_node:
            return parent_app_node.addMenu(self.label, **self.kwargs)

    def _setup_menu_item(self, parent_app_node=None):
        if parent_app_node:
            action = parent_app_node.addAction(self.label, **self.kwargs)
            action.setParent(parent_app_node)
            action.triggered.connect(self.run)
            return action

    def _setup_separator(self, parent_app_node=None):
        action = self._setup_menu_item(parent_app_node=parent_app_node)
        action.setSeparator(True)
        return action

    def teardown(self):
        """remove from menu"""
        self.app_node.deleteLater()

