from abc import abstractmethod, ABC
import unimenu.utils
from pathlib import Path
import logging
import re
import traceback


class MenuNode(object):
    """
    data class for menu items, this can be loaded in python in any app
    """
    unigue_names = set()
    # when creating a MenuNode from a config, we do MenuNode(**config), see MenuNode.load()
    def __init__(self, label=None, command=None, icon=None, tooltip=None, separator=False, items=None,
                 parent=None, parent_path=None, app_node=None, kwargs=None, data=None, id=None):
        """
        :param id: a unique name for the menu item. e.g. ANIMATION_EXPORTER. in qt this is objectName
        :param label: the label of the menu item
        :param command: the command to run when the menu item is clicked
        :param icon: the icon of the menu item
        :param tooltip: the tooltip of the menu item
        :param separator: if True, this menu item will be a separator
        :param items: a list of menu items
        :param kwargs: the kwargs to pass to the app-node instance
        :param data: custom data to store in the node, this is not used by unimenu, e.g. category, tags, etc
        :param parent_path: used to parent the tree to a parent, only used by the root-node
        :param app_node: HELPER linking the app menu node created by a MenuNode instance, tries to create a bidirectional link
        :param parent: HELPER linking the parent menu item, automatically set on children created from the 'items' kwarg
        """

        # config data
        self.label = label or ""
        self.command = command or ""
        self.icon = icon or ""
        self.tooltip = tooltip or ""
        self.separator = separator or False
        self.kwargs = kwargs or {}
        self.data = data or {}
        self.id = id or None

        # only the root node needs parent_path
        if parent_path:
            self.parent_path: str = parent_path.replace(" ", "_")
        else:
            self.parent_path = None
        # todo get parent path method

        # helpers
        self.parent: MenuNode = parent  # some implicit code use, pay attention to parent
        self.config_path = None  # the path to the config file that created this node todo do non root nodes populate this?
        
        # todo move to abstract
        self.app_node = app_node  # the app menu node created by this MenuNode instance
        self.app_node_parent = None  # root node only

        self._default_id()

        # since we pass parent, create items at end of init, so we first set all parent(self) attrs
        items = items or []
        self.items: list[MenuNodeAbstract] = [self.__class__(**item, parent=self) for item in items]

    def _default_id(self):
        # todo ideally should be unique
        
        if self.id:
            return

        label = self.label
        if not label:
            label = "TODO"  # todo unique number


        label = re.sub('[^0-9a-zA-Z]+', '_', label)  # replace non alphanumeric with _

        # add parent path to the id. ensures unique ids.
        # note that in e.g. unreal, the "name" is a type of id, that needs to be unique. but only one level deep.
        # so using id for name might result in repeated parent names. e.g. "parentA.ParentA_menuB"
        parent_names = []
        parent = self.parent
        while parent:
            parent_names.append(parent.id)  # todo, since id includes parent, adding parent id adds root parent multiple times
            parent = parent.parent
        parent_names.reverse()
        parent_names.append(label)
        self.id = "_".join(parent_names)
        # todo update this when parent changes, change to property
        # but if we rely on id to identify a node, then changing it when parent changes is bad
        # inform user that this string can change, they can save a pointer to the python instance instead

    @property
    def children(self):
        return self.items

    @children.setter
    def children(self, value):
        self.items = value

    @property
    def all_children(self):
        """return all children recursively"""
        children = []
        for child in self.children:
            children.append(child)
            children.extend(child.all_children)
        return children

    @property
    def all_command_nodes(self):
        """return: every menu entry that has a command"""
        commands = []
        for child in self.children:
            if child.command:
                commands.append(child)
            commands.extend(child.all_command_nodes)
        return commands

    def root(self):
        """return: the root node of the menu-tree"""
        # we use isinstance since sometimes parent is a string (or other type)
        # e.g. when the menu is loaded from a config file, the root node might have a string as parent
        if self.parent and isinstance(self.parent, MenuNode):
            return self.parent.root()
        return self

    def __dict__ (self):
        """return: a dict representation of this menu-node, used to save to a config file """
        config = {}
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
            child_configs = []
            for item in self.items:
                child_config = item.__dict__()
                child_config.pop("parent", None)  # we only need to save the parent for the top node
                child_configs.append(child_config)
            config["items"] = child_configs
        if self.parent_path and isinstance(self.parent_path, str):
            config["parent_path"] = self.parent_path
        if self.kwargs:
            config["kwargs"] = self.kwargs
        if self.data:
            config["data"] = self.data
        return config

    def run(self, *args):  # some apps pass args to the command. e.g. maya passes False
        """execute the command in self.command, which accepts a function or string"""
        try:
            if isinstance(self.command, str):
                # lambda: exec(self.command)
                exec(self.command)
            else:  # callable
                self.command()
        except Exception as e:
            traceback.print_exc()
            return e

    @classmethod
    def load(cls, arg):
        # if arg is a Path or string, load from config
        if isinstance(arg, (str, Path)):
            return cls.load_config(arg)
        # if arg is a dict, create a menu node from it
        elif isinstance(arg, dict):
            return cls(**arg)
        # if arg is a MenuNode, copy it
        elif isinstance(arg, MenuNode):
            return cls(**arg.__dict__())

    @classmethod
    def load_config(cls, config_path):
        data = unimenu.utils.load_config(config_path)
        menu_node = cls(**data)
        menu_node.config_path = config_path
        for node in menu_node.all_children:
            node.config_path = config_path
        return menu_node

    def print_tree(self, indent=0):
        """print a tree of the menu node labels"""
        _str = self.label

        if self.separator:
            if _str:
                _str = f"-- {_str} --"
            else:
                _str = "------"

        print("  " * indent + _str)
        for item in self.items:
            item.print_tree(indent + 1)


class MenuNodeAbstract(MenuNode, ABC):
    """
    Abstract class for app menu creation from a MenuNode tree
    """

    def setup(self, parent_app_node=None, backlink=True):
        """
        Instantiate a menu item in the app from the menu node data

        parent_app_node: app menu node to parent to, not a (uni)MenuNode!
        backlink: if True, add an attribute to the app node instance to the app node
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
        else:
            logging.warning("Can not create a MenuNode that has no command or children: " + self.label)

        # some apps, e.g. unreal, don't allow adding attributes dynamically
        if backlink:
            try:
                self.app_node.menu_node = self  # todo setproperty qt
            except AttributeError:
                logging.warning(f"Warning: could not set backlink on {self.app_node} to {self}")

        return self.app_node

    # todo consider moving to abstract, and func isntead of property
    # todo test with parent name in config for all apps
    # todo test with submenu name in config for all apps
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
    def teardown(self):
        """teardown the menu item"""
        pass
