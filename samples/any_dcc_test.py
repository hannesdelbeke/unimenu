"""
piece of test-code for copy/pasting, that should work in every dcc
"""

import sys
sys.path.append(r"C:\Users\hanne\OneDrive\Documents\repos\openmenu")
import unimenu


config = {"label": "UniMenu","items": [{"label": "Item 1","command": "print('Item 1')"},{"label": "Item 2","command": "print('Item 2')"}]}

config = {
    "label": "UniMenu",
    "items": [
        {
            "label": "Item 1",
            "command": "print('Item 1')"
        },
        {
            "label": "Item 2",
            "command": "print('Item 2')"
        }
    ]
}

app_menu_node = unimenu.setup(config)


# test teardown
node = unimenu.load(config)
app_node = node.setup()
node.teardown()
# bug when running this twice in a row, both menus are deleted
