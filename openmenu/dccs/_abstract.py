from abc import abstractmethod, ABC


class AbstractMenuMaker(ABC):

    @classmethod
    def _setup_menu_items(cls, parent_menu, items: list):
        """
        recursively add all menu items and submenus
        """
        created = []

        for item in items:

            if cls._is_separator(item):
                cls.add_separator(parent_menu)
                continue

            # get data
            label = item.get('label')
            command = item.get('command', None)
            tooltip = item.get('tooltip', None)
            icon = item.get('icon', None)

            if command:
                menu_item = cls.add_to_menu(parent_menu, label, command, icon, tooltip)
                created.append(menu_item)

            else:  # submenu
                items = item.get('items', [])
                sub_menu = cls.add_sub_menu(parent_menu, label)
                cls._setup_menu_items(sub_menu, items)
                created.append(sub_menu)

        return created  # only return top items, not submenus

    @classmethod
    @abstractmethod
    def setup_menu(cls, data):
        pass

    @classmethod
    @abstractmethod
    def add_sub_menu(cls, parent, label: str, tool_tip: str = ""):
        pass

    @classmethod
    @abstractmethod
    def add_to_menu(cls, parent, label: str, command: str, icon: str = "", tooltip: str = ""):
        pass

    @classmethod
    @abstractmethod
    def add_separator(cls, parent):
        pass

    @classmethod
    @abstractmethod
    def teardown_menu(cls):
        pass

    @staticmethod
    def _is_separator(item):
        return item == '---'
