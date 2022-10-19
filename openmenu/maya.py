import pymel.core as pm  # todo replace with cmds because it's faster


def setup_menu(data):
    menu = create_root_menu('OpenMenu')
    _setup_menu_items(menu, data.get('items'))


def _setup_menu_items(parent_menu, items: list):
    """
    recursively add all menu items and submenus
    """
    for item in items:
        label = item.get('label')
        print(item, label)
        command = item.get('command', None)
        if command:
            add_to_menu(parent_menu, label, command)
        else:  # submenu
            items = item.get('items', [])
            sub_menu = add_sub_menu(parent_menu, label)
            _setup_menu_items(sub_menu, items)


def create_root_menu(label, window_name='gMainWindow'):
    """
    Create a root menu in Maya
    label: str, the label of the menu
    window_name: str, the name of the window to attach the menu to
    """
    maya_window = pm.language.melGlobals[window_name]
    return pm.menu(label, parent=maya_window)


def add_sub_menu(parent, label: str):
    return pm.menuItem(subMenu=True, label=label, parent=parent)


def add_to_menu(parent, label: str, command: str):
    return pm.menuItem(label=label, command=command, parent=parent)


def breakdown():
    """remove from menu"""
    raise NotImplementedError("not yet implemented")
