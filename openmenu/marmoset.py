"""
marmoset doesn't support menu extensions,
so we create windows with buttons instead, submenus create new windows
"""

import mset

w = mset.UIWindow()
def setup_menu(data):
    global w
    _setup_menu_items(w, data.get('items'))


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


windows = []
def add_sub_menu(parent, label: str):
    dockable_window = mset.UIWindow()
    dockable_window.title = label

    global windows
    windows.append(dockable_window)

    return dockable_window



def add_to_menu(parent, label: str, command: str):
    def cmd():
        if isinstance(command, str):
            exec(command)
        else:
            command()
    # commands.append(cmd)

    button = mset.UIButton()
    button.text = label
    button.onClick = cmd
    parent.addElement(button)
    return button


def breakdown():
    """remove from menu"""
    raise NotImplementedError("not yet implemented")