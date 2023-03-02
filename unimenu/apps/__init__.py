"""
This submodule contains the app-specific implementations of the menu setup.
"""
import types
import contextlib
from typing import Optional
import logging
import importlib


class App:
    """
    Args:
    name: the name of the app, and also the name of the menu module.
    module: a unique python module only available in that app.
    """

    name = None
    module = None

    def __init__(self, name, module):
        self.name = name  # name of the unimenu module
        self.module = module  # a unique module only importable in the app

    @property
    def menu_module(self) -> types.ModuleType:
        """
        the app-specific menu module, lazy import prevents import issues with other apps
        """
        return importlib.import_module(f"unimenu.apps.{self.name}")

    @property
    def menu_node_class(self) -> "unimenu.apps._abstract.MenuNodeAbstract":  # " in typehint to avoid circular import
        """get the app-specific menu node class"""
        name = self.name.replace("_", " ").title().replace(" ", "")  # convert lower_case to CamelCase
        return getattr(self.menu_module, "MenuNode" + name)  # get the MenuNode class from the app module


class SupportedApps:
    """Apps supported by this module, no need to add non QT apps here"""

    # app -> digital content creation (software)

    BLENDER = App(name="blender", module="bpy")
    MAYA = App(name="maya", module="maya")  # pymel can be slow to import
    UNREAL = App(name="unreal", module="unreal")
    MAX = App(name="max", module="pymxs")
    KRITA = App(name="krita", module="krita")
    SUBSTANCE_DESIGNER = App(name="substance_designer", module="pysbs")
    SUBSTANCE_PAINTER = App(name="substance_painter", module="substance_painter")
    MARMOSET = App(name="marmoset", module="mset")

    QT = App("qt", None)

    # ALL = [BLENDER, MAYA, UNREAL, KRITA, SUBSTANCE_PAINTER, MAX, MARMOSET]
    NON_QT = [BLENDER, UNREAL, SUBSTANCE_PAINTER, MARMOSET]


def detect_app() -> Optional[App]:
    """
    detect which app is currently running
    returns QT if no custom supported app is detected
    """
    for app in SupportedApps.NON_QT:
        with contextlib.suppress(ImportError):
            __import__(app.module)
            logging.debug(f"UNIMENU: detected {app.name}")
            return app
    # logging.info("UNIMENU: no custom App detected, falling back to QT")
    return SupportedApps.QT

