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

sys.path.append(r"C:\Users\hanne\OneDrive\Documents\repos\unimenu")

import unimenu
from unimenu.apps import detect_app
from importlib import reload
from pathlib import Path


def create_test_menus():
    app = detect_app()
    reload(app.menu_module)

    config = Path(unimenu.__file__).parent.parent / "samples/config.json"
    # in substance painter, Path(unimenu.__file__) does not return this file's location but instead:
    # 'C:\\Users\\hanne\\OneDrive\\Documents\\Adobe\\Adobe Substance 3D Painter\\python\\modules\\samples\\config.json'
    config = Path(r"C:\Users\hanne\OneDrive\Documents\repos\unimenu\samples\config.json")

    # add single entry to menu
    menu1 = unimenu.add_item("menu1")

    # add menu tree from config
    menu2 = unimenu.setup_config(config)[0]

    # print(menu2)
    # in susbtance painter, this throws a
    # [Python] RuntimeError: Internal C++ object (PySide2.QtWidgets.QMenu) already deleted.

    # add submenu to menu
    sub_menu1 = unimenu.add_item("menu3", parent=menu2)

    # add action to menu
    menu_entry = unimenu.add_item("print hi", command="print('hi')", parent=menu2)

    print(menu_entry)
    # TODO fix: in susbtance painter, this throws a
    #  [Python] RuntimeError: Internal C++ object (PySide2.QtWidgets.QAction) already deleted.
    # TODO test, think this might be resolved now with the any_dcc_test.py & qt implementation.

create_test_menus()
