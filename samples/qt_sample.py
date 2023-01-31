"""
a pure qt demo
"""

import unimenu.dccs.qt
from PySide2 import QtWidgets

data = {
    'items':
    [
        {
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
                ],
            'label': 'Tools'
        }
    ]
}

# create placeholder qt window
app = QtWidgets.QApplication([])
window = QtWidgets.QMainWindow()
menu = window.menuBar()

# setup tools menu from config
unimenu.dccs.qt.QtMenuMaker.setup_menu(data, parent=menu)

window.show()
app.exec_()
