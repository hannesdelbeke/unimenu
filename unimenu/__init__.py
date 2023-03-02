"""
Create custom menus in a uniform way between multiple Apps.
"""

from unimenu.core import *


__all__ = [
    'setup',
    "setup_module",
    "teardown_menu",
]


# main menu is the main menu bar
# window is the window that contains the main menu bar
# parent can be the main menu bar or a submenu, or a window depending on app
# TODO standardize this
