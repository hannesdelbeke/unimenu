"""
sample for testing
run in Krita from the menu: Tools/scripts/scripter
"""
from openmenu.dccs import detect_dcc
from importlib import reload
from pathlib import Path
import openmenu
import sys


dcc = detect_dcc()
reload(dcc.menu_module)

sys.path.append(r"C:\Users\hanne\OneDrive\Documents\repos\openmenu")
config = Path(openmenu.__file__).parent.parent / "samples/config.json"

# add single entry to menu
menu1 = openmenu.add_item("menu1")

# add menu tree from config
menu2 = openmenu.setup_config(config)[0]
print(menu2)

# add submenu to menu
openmenu.add_item("menu3", parent=menu2)

# add action to menu
menu_entry = openmenu.add_item("print hi", command="print('hi')", parent=menu2)
print(menu_entry)

