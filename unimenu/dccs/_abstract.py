from abc import abstractmethod, ABC
import unimenu.utils


class AbstractMenuMaker(ABC):
    @classmethod
    def _setup_menu_items(cls, parent, items: list):
        """
        recursively add all menu items and submenus
        """
        # created = []

        for item in items:

            label = item.get("label")
            icon = item.get("icon", None)
            command = item.get("command", None)
            tooltip = item.get("tooltip", None)

            if cls._is_separator(item):
                cls.add_separator(parent, label=label)
                continue

            elif command:
                menu_item = cls.add_to_menu(parent, label, command, icon, tooltip)
                # created.append(menu_item)

            else:  # submenu
                items = item.get("items", [])
                sub_menu = cls.add_sub_menu(parent, label)
                cls._setup_menu_items(sub_menu, items)
                # created.append(sub_menu)

        # return created  # only return top items, not submenus

    @classmethod
    @abstractmethod
    def setup_menu(cls, data):
        # return an object that represents the menu item created, and can be parented too
        pass

    @classmethod
    @abstractmethod
    def add_sub_menu(cls, parent, label: str, tool_tip: str = None):
        # return an object that represents the menu item created, and can be parented too
        pass

    @classmethod
    @abstractmethod
    def add_to_menu(cls, parent, label: str, command: str, icon: str = None, tooltip: str = None):
        # return an object that represents the menu item created, and can be parented too
        pass

    @classmethod
    @abstractmethod
    def add_separator(cls, parent, label: str = None):
        # no need to return separator object, but return it if possible to future-proof
        pass

    @classmethod
    @abstractmethod
    def teardown_menu(cls):
        pass

    @staticmethod
    def _is_separator(item):
        return item.get("separator", False)


class MenuNode(object):
    """
    data class for menu items, this can be loaded in python in any app
    """
    def __init__(self, label=None, command=None, icon=None, tooltip=None, separator=False, items=None,
                 parent=None, parent_path=None, app_node=None):

        # config data
        self.label = label or ""
        self.command = command or ""
        self.icon = icon or ""
        self.tooltip = tooltip or ""
        self.separator = separator or False
        items = items or []
        self.items: list[MenuNodeAbstract] = [self.__class__(**item) for item in items]

        # only top node can have parent in config, so this is not needed
        self.parent_path = parent_path  # only the root node needs this
        # todo get parent path method

        # helpers
        self.parent: MenuNode = parent  # some implicit code use, pay attention to parent
        self.config_path = None  # the path to the config file that created this node
        
        # todo move to abstract
        self.app_node = app_node  # the app menu node created by this MenuNode instance
        self.app_node_parent = None  # root node only

    @property
    def children(self):
        return self.items

    @children.setter
    def children(self, value):
        self.items = value

    def root(self):
        """Return the root node of the menu-tree"""
        # we use isinstance since sometimes parent is a string (or other type)
        # e.g. when the menu is loaded from a config file, the root node might have a string as parent
        if self.parent and isinstance(self.parent, MenuNode):
            return self.parent.root()
        return self

    def __dict__ (self):
        # used to save back to a config file
        config = {
        }
        if self.label:
            config["label"] = self.label
        if self.command:
            config["command"] = self.command
        if self.icon:
            config["icon"] = self.icon
        if self.tooltip:
            config["tooltip"] = self.tooltip
        if self.separator:
            config["separator"] = self.separator
        if self.items:
            configs = []
            for item in self.items:
                config = item.__dict__()
                config.pop("parent", None)  # we only need to save the parent for the top node
                configs.append(config)
        if self._parent and isinstance(self._parent, str):
            config["parent_path"] = self.config_parent
        return config

    def run(self):
        """execute the command in self.command, which accepts a function or string"""
        if isinstance(self.command, str):
            lambda: exec(self.command)
        else:  # callable
            self.command()

    @classmethod
    def load(cls, config_path):
        data = unimenu.utils.load_config(config_path)
        menu_node = cls(**data)
        menu_node.config_path = config_path
        return menu_node

    def print_tree(self, indent=0):
        """print a tree of the menu node labels"""
        print("  " * indent + self.label)
        for item in self.items:
            item.print_tree(indent + 1)


class MenuNodeAbstract(MenuNode, ABC):
    """
    Abstract class for app menu creation from a MenuNode tree
    """

    def setup(self, parent_app_node=None):
        """
        Instantiate a menu item in the app from the menu node data
        parent: app menu to parent to, not a MenuNode!
        """
        parent_app_node = parent_app_node or self._default_root_parent

        if self.separator:
            self.app_node = self._setup_separator(parent_app_node=parent_app_node)

        elif self.command:  # menu item
            self.app_node = self._setup_menu_item(parent_app_node=parent_app_node)

        elif self.items:  # submenu
            self.app_node = self._setup_sub_menu(parent_app_node=parent_app_node)
            for item in self.items:
                item.setup(parent_app_node=self.app_node)

        return self.app_node

    @property
    def _default_root_parent(self):
        """get the default parent for the root node, optional method"""
        return None

    @abstractmethod
    def _setup_sub_menu(self, parent_app_node=None):
        """instantiate & parent a sub menu"""
        pass

    @abstractmethod
    def _setup_menu_item(self, parent_app_node=None):
        """instantiate & parent a menu item"""
        pass

    @abstractmethod
    def _setup_separator(self, parent_app_node=None):
        """instantiate & parent a separator"""
        pass

    @abstractmethod
    def _teardown(self):
        """teardown the menu item"""
        pass
