from unimenu.apps._abstract import MenuNodeAbstract
import hiero
from PySide2 import QtGui


class MenuNodeHiero(MenuNodeAbstract):

    @property
    def _default_root_parent(self):
        menubar = None
        if self.parent_path:
            try:
                menubar = hiero.ui.findMenuAction(self.parent_path)
            except Exception:
                menubar = None
        
        if not menubar:
            menu = hiero.ui.menuBar()
        else:
            menu = menubar.menu()
        return menu

    def _setup_sub_menu(self, parent_app_node=None):
        if not self.label:
            self.label = "custom_menu"
        if parent_app_node:
            return parent_app_node.addMenu(self.label)
        else:  # make a normal sub menu
            return hiero.ui.menuBar().addMenu(self.label)

    def _setup_menu_item(self, parent_app_node=None):
        menu_action = parent_app_node.addAction(self.label)
        if self.icon:
            menu_action.setIcon(QtGui.QIcon(self.icon))
        menu_action.triggered.connect(self.run)

    def _setup_separator(self, parent_app_node=None):
        if parent_app_node:
            parent_app_node.addSeparator()

    def teardown(self):
         raise NotImplementedError("not yet implemented")
