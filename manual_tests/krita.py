"""
sample for testing
run in Krita from the menu: Tools/scripts/scripter
"""
import sys
sys.path.append(r"C:\Users\hanne\OneDrive\Documents\repos\openmenu")

from importlib import reload
import openmenu
import openmenu.dccs.krita as k
reload(k)
from pathlib import Path

# add single entry to menu
menu1 = openmenu.add_item("menu1")

# add menu tree from config
config = Path(openmenu.__file__).parent.parent / "samples/config.json"
menu2 = openmenu.setup_config(config)[0]
print(menu2)

# add submenu to menu
openmenu.add_item("menu3", parent=menu2)

# add action to menu
menu_entry = openmenu.add_item("print hi", command="print('hi')", parent=menu2)
print(menu_entry)

