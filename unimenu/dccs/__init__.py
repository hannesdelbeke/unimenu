"""
This submodule contains the dcc-specific implementations of the menu setup.
"""
import types
import contextlib
from typing import Optional
import logging
import importlib


class DCC:
    """
    Args:
    name: the name of the dcc, and also the name of the menu module.
    module: a unique python module only available in that dcc.
    """

    name = None
    module = None

    def __init__(self, name, module):
        self.name = name  # name of the unimenu module
        self.module = module  # a unique module only importable in the dcc

    @property
    def menu_module(self) -> types.ModuleType:
        """
        the dcc-specific menu module, lazy import prevents import issues with other dccs
        """
        return importlib.import_module(f"unimenu.dccs.{self.name}")

    @property
    def menu_node_class(self) -> "unimenu.dccs._abstract.MenuNodeAbstract":  # " in typehint to avoid circular import
        """get the dcc-specific menu node class"""
        name = self.name.replace("_", " ").title().replace(" ", "")  # convert lower_case to CamelCase
        return getattr(self.menu_module, "MenuNode" + name)  # get the MenuNode class from the dcc module


class SupportedDCCs:
    """DCCs supported by this module"""

    # dcc -> digital content creation (software)

    BLENDER = DCC(name="blender", module="bpy")
    MAYA = DCC(name="maya", module="maya")  # pymel can be slow to import
    UNREAL = DCC(name="unreal", module="unreal")
    MAX = DCC(name="max", module="pymxs")
    KRITA = DCC(name="krita", module="krita")
    SUBSTANCE_DESIGNER = DCC(name="substance_designer", module="pysbs")
    SUBSTANCE_PAINTER = DCC(name="substance_painter", module="substance_painter")
    MARMOSET = DCC(name="marmoset", module="mset")

    QT = DCC("qt", None)

    ALL = [BLENDER, MAYA, UNREAL, KRITA, SUBSTANCE_PAINTER, MAX, MARMOSET]


def detect_dcc() -> Optional[DCC]:
    """detect which dcc is currently running"""
    for dcc in SupportedDCCs.ALL:
        with contextlib.suppress(ImportError):
            __import__(dcc.module)
            logging.debug(f"UNIMENU: detected {dcc.name}")
            return dcc
    logging.warning("UNIMENU: no supported DCC detected, falling back to QT")
    return SupportedDCCs.QT

