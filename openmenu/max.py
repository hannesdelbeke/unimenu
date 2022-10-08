# """
# if True:
#     ## add to path
#     import sys
#     sys.path.append(r'C:\Users\hanne\OneDrive\Documents\repos\openmenu')
#     sys.path.append(r'C:\Users\hanne\OneDrive\Documents\repos\BlenderTools\modules\vendor')  # yaml
#
#     cfg = r"C:\Users\hanne\OneDrive\Documents\repos\openmenu\samples\config.json"
#     import openmenu
#     import openmenu.core as c
#
#     import openmenu.max as b
#     from importlib import reload
#     reload(b)
#     reload(c)
#     reload(openmenu)
#
#     openmenu.config_setup(cfg)
# """

# 3ds max

from pymxs import runtime as rt
menuMan = rt.menuMan


def setup_menu(data):
    mainMenuBar = menuMan.getMainMenuBar()
    _setup_menu_items(mainMenuBar, data.get('items'))
    menuMan.updateMenuBar()


def _setup_menu_items(parent, items: list):
    """
    recursively add all menu items and submenus
    """
    for item in items:
        label = item.get('label')
        tooltip = item.get('tooltip')
        command = item.get('command', None)
        if command:
            pass
            add_to_menu(parent, label, command, tooltip)
        else:  # submenu
            items = item.get('items', [])
            sub_menu = add_sub_menu(parent, label)
            _setup_menu_items(sub_menu, items)


def add_sub_menu(parent, label):
    sub_menu = menuMan.createMenu(label)
    sub_menu_item = menuMan.createSubMenuItem(label, sub_menu)
    parent.addItem(sub_menu_item, -1)
    return sub_menu


def add_to_menu(parent, label: str, command: str, tooltip: str = ''):
    macro_name, macro_category = create_macro(label, command)
    item = rt.menuMan.createActionItem(macro_name, macro_category)
    parent.addItem(item, -1)  # item index


counter = -1


def add_callable_to_maxscript(command):
    """
    add to runtime, creating a callable var in maxscript
    command: (str or callable) execute string as python code, or run callable
    """
    global counter  # counter guarantees unique macro names
    counter += 1

    def _execute_command():
        if isinstance(command, str):
            exec(command)
        else:
            command()

    cmd_name = f'openmenu_{counter}'
    setattr(rt, cmd_name, _execute_command)  # add to runtime, creating a callable var in maxscript

    return cmd_name


def create_macro(label, command):
    """
    create a macroscript exposed to maxscript
    """
    cmd_name = add_callable_to_maxscript(command)

    macro_name = cmd_name
    macro_category = 'OpenMenu'
    macro_tooltip = 'This is a tooltip'  # TODO this doesn't work
    macro_text = label
    macro_content = cmd_name + '()'
    macro_id = rt.macros.new(macro_category, macro_name, macro_tooltip, macro_text, macro_content)
    return macro_name, macro_category


def breakdown():
    """remove from menu"""
    raise NotImplementedError("not yet implemented")

# menu man pymxs official https://help.autodesk.com/view/MAXDEV/2022/ENU/?guid=Max_Python_API_using_pymxs_pymxs_macroscripts_menus_html
# maxscript menuman ref https://help.autodesk.com/view/3DSMAX/2017/ENU/?guid=__files_GUID_258F6015_6B45_4A87_A7F5_BB091A2AE065_htm
