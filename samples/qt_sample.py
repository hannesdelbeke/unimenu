"""
a pure qt demo
"""

import unimenu.apps.qt
from PySide2 import QtWidgets

data = {
    'label': 'Tools',
    'items':
        [
            {
                'command': 'print("hello 1")',
                'label': 'tool1',
                "icon": ":/qt-project.org/styles/commonstyle/images/up-32.png",
                "tooltip": "tooltip"
            },
            {
                'label': 'label',
                'separator': True,
                "icon": ":/qt-project.org/styles/commonstyle/images/up-32.png",
                "tooltip": "tooltip separator"
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

# create qt window for demo
app = QtWidgets.QApplication([])
window = QtWidgets.QMainWindow()
menu = window.menuBar()

# test smart setup
q_node = unimenu.setup(data)
menu.addMenu(q_node)

# setup tools menu from config
menu_node = unimenu.apps.qt.MenuNodeQt(**data)
menu_node.print_tree()
# Tools
#   tool1
#   tool2

# create the Qt menu & add it to the menu bar
a = menu_node.setup(parent_app_node=menu)

b = menu_node.setup()
b.setTitle("Tools2")
menu.addMenu(b)

# run demo
window.show()
app.exec_()
