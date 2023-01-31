from abc import abstractmethod, ABC


class AbstractMenuMaker(ABC):
    @classmethod
    def _setup_menu_items(cls, parent, items: list):
        """
        recursively add all menu items and submenus
        """
        created = []

        for item in items:

            label = item.get("label")

            if cls._is_separator(item):
                cls.add_separator(parent, label=label)
                continue

            # get data
            icon = item.get("icon", None)
            command = item.get("command", None)
            tooltip = item.get("tooltip", None)

            if command:
                menu_item = cls.add_to_menu(parent, label, command, icon, tooltip)
                created.append(menu_item)

            else:  # submenu
                items = item.get("items", [])
                sub_menu = cls.add_sub_menu(parent, label)
                cls._setup_menu_items(sub_menu, items)
                created.append(sub_menu)

        return created  # only return top items, not submenus

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


class MenuNode():
    def __init__(self, label=None, command=None, icon=None, tooltip=None, separator=False, items=None, config=None,
                 parent=None):
        if not config:
            config = {}

        # config data
        self.label = label or config.get("label", "")
        self.command = command or config.get("command", "")
        self.icon = icon or config.get("icon", "")
        self.tooltip = tooltip or config.get("tooltip", "")
        self.separator = separator or config.get("separator", False)
        self.items = items or [MenuNode(config=item) for item in config.get("items", [])]

        # helpers
        self._parent = parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        # check if value is a MenuNode
        if not isinstance(value, MenuNode):
            raise TypeError("Parent must be a MenuNode")
        self._parent = value

    @property
    def children(self):
        return self.items

    @children.setter
    def children(self, value):
        self.items = value

    def root(self):
        """Return the root node of the menu-tree"""
        if self.parent:
            return self.parent.root()
        return self

    def __dict__ (self):
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
            config["items"] = [item.__dict__() for item in self.items]
        return config


# class MenuItem(Menu):
#     pass

# def _is_separator(item):
#     return item.get("separator", False)


# def load_menu(parent, items: list):
#     created = []
#
#     for item in items:
#         menu = MenuNode(config=item)
#
#
#
#
#         label = item.get("label")
#
#         if cls._is_separator(item):
#             cls.add_separator(parent, label=label)
#             continue
#
#         # get data
#         icon = item.get("icon", None)
#         command = item.get("command", None)
#         tooltip = item.get("tooltip", None)
#
#         if command:
#             menu_item = cls.add_to_menu(parent, label, command, icon, tooltip)
#             created.append(menu_item)
#
#         else:  # submenu
#             items = item.get("items", [])
#             sub_menu = cls.add_sub_menu(parent, label)
#             cls._setup_menu_items(sub_menu, items)
#             created.append(sub_menu)
#
#     return created  # only return top items, not submenus




