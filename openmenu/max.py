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

# TODO issues with yaml in 3dsmax, test

from pymxs import runtime as rt
menuMan = rt.menuMan


def setup_menu(data):

    items = data.get('items')
    mainMenuBar = menuMan.getMainMenuBar()
    _setup_menu_items(mainMenuBar, data.get('items'))
    menuMan.updateMenuBar()
    # for item in items:
    #     label = item.get('label')
    #
    #      = menuMan.getMainMenuBar()
    #
    #     menu = menuMan.createMenu(label)
    #     menuMan.updateMenuBar()
    #
    #     continue
    #     # if MaxPlus.MenuManager.MenuExists(label):
    #     #     print("Menu already exists: " + label)
    #     #     continue
    #     #     # TODO add replace option
    #
    #     # menu_builder = MaxPlus.MenuBuilder(label)


def _setup_menu_items(parent, items: list):
    """
    recursively add all menu items and submenus
    """
    for item in items:
        label = item.get('label')
        command = item.get('command', None)
        if command:
            pass
            add_to_menu(parent, label, command)
        else:  # submenu
            print(item, label)
            items = item.get('items', [])
            sub_menu = add_sub_menu(parent, label)
            _setup_menu_items(sub_menu, items)

def add_sub_menu(parent, label):
    sub_menu = menuMan.createMenu(label)
    sub_menu_item = menuMan.createSubMenuItem(label, sub_menu)
    parent.addItem(sub_menu_item, -1)
    return sub_menu

counter = -1
commands = {}
rt.run_openmenu = setup_menu

def add_to_menu(parent, label: str, command: str):
    global counter
    global commands
    counter += 1

    commands[label] = command
    def _execute_command():
        # run string as python
        exec(command)

    cmd_name = f'openmenu_{counter}'
    setattr(rt, cmd_name, _execute_command)



    maxscript_command = f'python.execute("{command}")'
    print(maxscript_command)
    macro_name = 'OpenMenu_' + label.lower().replace('_', '') + str(counter)
    macro_category = 'OpenMenu'
    # create_macro(category=macro_category,
    #              name=macro_name,
    #              tool_tip=label,
    #              button_text=label,
    #              script=cmd_name+'()')






    # Our Py function:
    def myfunc():
        print('hello testrld')

    cmd_name = f'openmenu_{counter}'
    setattr(rt, cmd_name, _execute_command)
    # Connect to a gobal in the runtime:
    # rt.mxs_hello = _execute_command

    macroscript_name = cmd_name #'My_Macroscript'

    macroscript_category = 'Test'
    macroscript_tooltip = 'This is a tooltip'
    # this sets the text used for any menus or ui controls
    # associated with this macroscript
    macroscript_text = label
    # this is a MAXSCript:
    macroscript_content = cmd_name + '()'

    macro_id = rt.macros.new(macroscript_category, macroscript_name, macroscript_tooltip, macroscript_text,
                             macroscript_content)
    print(macro_id)
    menu_item = rt.menuMan.createActionItem(macroscript_name, macroscript_category)
    item = menu_item





    # item = menuMan.createActionItem(label, command)
    # item = menuMan.createActionItem(macro_name, macro_category)
    print("adding action to parent", parent, item)
    parent.addItem(item, -1)  # item index


def create_macro(category, name, tool_tip, button_text, script):
    print("create_macro", category, name, tool_tip, button_text, script)
    macro_id = rt.macros.new(category, name, tool_tip, button_text, script)
    return macro_id


# def add_sub_menu(parent_menu_builder, label: str):
#     menu_builder = MaxPlus.MenuBuilder(label)
#     sub_menu = menu_builder.Create()
#     parent_menu_builder.AddSubMenu(sub_menu)
#     return sub_menu
#
#
# def add_to_menu(parent_menu_builder, label: str, command: str):
#     parent_menu_builder.AddItem(label, command)
#     # AddItem(MenuBuilder, ActionItem)


def breakdown():
    """remove from menu"""
    raise NotImplementedError("not yet implemented")

# menu man pymxs official https://help.autodesk.com/view/MAXDEV/2022/ENU/?guid=Max_Python_API_using_pymxs_pymxs_macroscripts_menus_html
# maxscript menuman ref https://help.autodesk.com/view/3DSMAX/2017/ENU/?guid=__files_GUID_258F6015_6B45_4A87_A7F5_BB091A2AE065_htm
