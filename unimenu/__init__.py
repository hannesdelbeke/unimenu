"""
Create custom menus in a uniform way between multiple DCCs.
"""

from unimenu.core import *


__all__ = [
    # 'setup',
    "setup_config",
    "setup_dict",
    "setup_module",
    "add_item",
    # 'breakdown',
]


# main menu is the main menu bar
# window is the window that contains the main menu bar
# parent can be the main menu bar or a submenu, or a window depending on dcc
# TODO standardize this
