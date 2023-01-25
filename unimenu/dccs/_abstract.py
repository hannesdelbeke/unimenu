from abc import abstractmethod, ABC


class AbstractMenuMaker(ABC):
    @classmethod
    def _setup_menu_items(cls, parent, items: list):
        """
        recursively add all menu items and submenus
        """
        created = []

        for item in items:

            try:  # this fails to run on strings (separators)
                label = item.get("label")
            except:
                label = None

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
        return item == "---" or item.get("separator", False)
