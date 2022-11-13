"""
generate menus in 3ds max

generated menus are persistent between sessions!
"""

from pymxs import runtime as rt
from pathlib import Path


counter = -1


def setup_menu(data):
    mainMenuBar = rt.menuMan.getMainMenuBar()
    _setup_menu_items(mainMenuBar, data.get('items'))
    rt.menuMan.updateMenuBar()


def _setup_menu_items(parent, items: list):
    """
    recursively add all menu items and submenus
    """
    for item in items:
        label = item.get('label')
        tooltip = item.get('tooltip')
        command = item.get('command', None)
        if command:
            add_to_menu(parent, label, command, tooltip)
        else:  # submenu
            items = item.get('items', [])
            sub_menu = add_sub_menu(parent, label)
            _setup_menu_items(sub_menu, items)


def add_sub_menu(parent, label):
    sub_menu = rt.menuMan.createMenu(label)
    sub_menu_item = rt.menuMan.createSubMenuItem(label, sub_menu)
    parent.addItem(sub_menu_item, -1)
    return sub_menu


def add_to_menu(parent, label: str, command: str, tooltip: str = ''):
    # todo generated menus are persistent between sessions!
    #  this does not match the behavior of other DCCs currently
    #  a macro is created at C:\Users\hanne\AppData\Local\Autodesk\3dsMax\2024 - 64bit\ENU\usermacros\
    macro_name, macro_category = create_macro(label, command)
    # todo handle case when we create a macro with the same name as an existing macro
    # since actionitems are based of macro names, we can't have two actionitems with the same name
    item = rt.menuMan.createActionItem(macro_name, macro_category)
    parent.addItem(item, -1)  # item index


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


def teardown():
    """remove from menu"""

    # todo remove dynamically created macros
    macros_path = Path(rt.pathConfig.getDir(rt.name('Additional Macros')))
    # delete all files containing openmenu in their name, in the folder with path macros_path
    for file in macros_path.glob('openmenu*'):
        file.unlink()

    # get info from macros and remove from menu
    # track submenus created, across sessions

    raise NotImplementedError("not yet implemented")


def teardown_by_name(name):
    # todo since this is based on remove menu by name, ensure we don't remove default max menus.
    #  use some kind of openmenu append to name on creation
    #  also handle duplicate names
    menu_interface = rt.menuMan.findMenu(name)
    rt.menuMan.unRegisterMenu(menu_interface)

# menu man pymxs official https://help.autodesk.com/view/MAXDEV/2022/ENU/?guid=Max_Python_API_using_pymxs_pymxs_macroscripts_menus_html
# maxscript menuman ref https://help.autodesk.com/view/3DSMAX/2017/ENU/?guid=__files_GUID_258F6015_6B45_4A87_A7F5_BB091A2AE065_htm
