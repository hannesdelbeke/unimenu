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
            },
            {
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
        ]
}

# setup tools menu from config
menu_node = unimenu.dccs.qt.MenuNodeQt(**data)
menu_node.print_tree()
# Tools
#   tool1
#   tool2

# create qt window for demo
app = QtWidgets.QApplication([])
window = QtWidgets.QMainWindow()
menu = window.menuBar()

# create the Qt menu & add it to the menu bar
a = menu_node.setup(parent_app_node=menu)

b = menu_node.setup()
b.setTitle("Tools2")
menu.addMenu(b)

# run demo
window.show()
app.exec_()
