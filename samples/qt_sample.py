"""
a pure qt demo
"""

import unimenu.dccs.qt
from PySide2 import QtWidgets

data = {
    'label': 'Tools',
    'items':
        [
            {
                'command': 'print("hello 1")',
                'label': 'tool1'
            },
            {
                'command': 'print("hello 2")',
                'label': 'tool2'
            }
        ]
}

# setup tools menu from config
menu_node = unimenu.dccs.qt.QtMenuNode(**data)
# create placeholder qt window
app = QtWidgets.QApplication([])
window = QtWidgets.QMainWindow()
menu = window.menuBar()

# setup tools menu from config
unimenu.dccs.qt.QtMenuMaker.setup_menu(data, parent=menu)

window.show()
app.exec_()
