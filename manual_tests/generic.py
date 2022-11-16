"""
sample for testing

run in Krita from the menu: Tools/scripts/scripter

in substance painter,
open Python/Plugins folder
place substance painter test in the folder
click Python/Reload plugins folder
a test entry should appear in the menu, click it to run the test
"""

import sys
sys.path.append(r"C:\Users\hanne\OneDrive\Documents\repos\openmenu")

import openmenu
from openmenu.dccs import detect_dcc
from importlib import reload
from pathlib import Path


def create_test_menus():
    dcc = detect_dcc()
    reload(dcc.menu_module)


    config = Path(openmenu.__file__).parent.parent / "samples/config.json"
    # in substance painter, Path(openmenu.__file__) does not return this file's location but instead:
    # 'C:\\Users\\hanne\\OneDrive\\Documents\\Adobe\\Adobe Substance 3D Painter\\python\\modules\\samples\\config.json'
    config = Path(r"C:\Users\hanne\OneDrive\Documents\repos\openmenu\samples\config.json")

    # add single entry to menu
    menu1 = openmenu.add_item("menu1")

    # add menu tree from config
    menu2 = openmenu.setup_config(config)[0]

    # print(menu2)
    # in susbtance painter, this throws a
    # [Python] RuntimeError: Internal C++ object (PySide2.QtWidgets.QMenu) already deleted.

    # add submenu to menu
    sub_menu1 = openmenu.add_item("menu3", parent=menu2)

    # add action to menu
    menu_entry = openmenu.add_item("print hi", command="print('hi')", parent=menu2)

    print(menu_entry)
    # in susbtance painter, this throws a
    # [Python] RuntimeError: Internal C++ object (PySide2.QtWidgets.QAction) already deleted.


# if __name__ == "__main__":
#     run_tests()