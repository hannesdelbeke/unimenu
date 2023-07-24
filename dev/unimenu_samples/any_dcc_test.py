"""
piece of test-code for copy/pasting, that should work in every app
"""

import sys
sys.path.append(r"C:\Users\hanne\OneDrive\Documents\repos\openmenu")
import unimenu
import unimenu.apps.qt as q
import unimenu.apps._abstract as a
from importlib import reload
reload(q)
reload(a)
reload(unimenu)


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


config = {
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

app_menu_node = unimenu.setup(config)


# test teardown
node = unimenu.load(config)
app_node = node.setup()
node.teardown()
