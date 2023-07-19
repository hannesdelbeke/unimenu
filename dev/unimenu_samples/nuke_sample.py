"""
a pure qt demo
"""

import unimenu.apps.nuke
from PySide2 import QtWidgets

data = {
    'label': 'Tools',
    'items':
        [
            {
                'command': 'print("hello 1")',
                'label': 'tool1',
            },
            {
                'separator': True,
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

nodes_menu_data = {
    "parent_path": "Nodes",
    'label': 'Tools',
    'items':
        [
            {
                'command': 'print("hello 1")',
                'label': 'tool1',
            },
            {
                'separator': True,
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

# create a nuke menu

import unimenu
from unimenu.apps import SupportedApps


# config = Path(unimenu.__file__).parent.parent / "samples/config.json"
unimenu.setup(data, SupportedApps.NUKE)

# Create to Nodes

unimenu.setup(nodes_menu_data, SupportedApps.NUKE)
