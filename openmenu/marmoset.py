"""
marmoset doesn't support menu extensions,
so we create windows with buttons instead, submenus create new windows
"""

import mset


def setup_menu(data):
    _setup_menu_items(None, data.get('items'))


def _setup_menu_items(parent_menu, items: list):
    """
    recursively add all menu items and submenus
    """
    for item in items:
        label = item.get('label')
        print(item, label)
        command = item.get('command', None)
        if command:
            pass
            add_to_menu(parent_menu, label, command)
        else:  # submenu
            items = item.get('items', [])
            sub_menu = add_sub_menu(parent_menu, label)
            _setup_menu_items(sub_menu, items)


windows = []


def add_sub_menu(parent, label: str):
    global windows
    if not parent:
        window = mset.UIWindow(label)
        # save window in a global to prevent garbage collection
        windows.append(window)
        return window

    settings_drawer_ui = mset.UIDrawer(name=label)
    settings_drawer = mset.UIWindow(name="", register=False)
    settings_drawer_ui.containedControl = settings_drawer

    parent.addReturn()  # work vertically since else window looks bad
    parent.addElement(settings_drawer_ui)
    parent.addReturn()

    return settings_drawer


def add_to_menu(parent, label: str, command: str):
    def cmd():
        if isinstance(command, str):
            exec(command)
        else:
            command()

    button = mset.UIButton()
    button.text = label
    button.onClick = cmd
    parent.addElement(button)
    return button


def breakdown():
    """remove from menu"""
    raise NotImplementedError("not yet implemented")
