"""
This submodule contains the dcc-specific implementations of the menu setup.
"""

import warnings
from collections import namedtuple
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
    def menu_module(self):
        """
        the dcc-specific menu module, lazy import prevents import issues with other dccs
        """
        return importlib.import_module(f"unimenu.dccs.{self.name}")


class SupportedDCCs:
    """DCCs supported by this module"""

    # dcc -> digital content creation (software)

    BLENDER = DCC("blender", "bpy")
    MAYA = DCC("maya", "maya")  # pymel can be slow to import
    UNREAL = DCC("unreal", "unreal")
    MAX = DCC("max", "pymxs")
    KRITA = DCC("krita", "krita")
    SUBSTANCE_DESIGNER = DCC("substance_designer", "pysbs")
    SUBSTANCE_PAINTER = DCC("substance_painter", "substance_painter")
    MARMOSET = DCC("marmoset", "mset")

    ALL = [BLENDER, MAYA, UNREAL, KRITA, SUBSTANCE_PAINTER, MAX, MARMOSET]


def detect_dcc() -> Optional[DCC]:
    """detect which dcc is currently running"""
    for dcc in SupportedDCCs.ALL:
        with contextlib.suppress(ImportError):
            logging.debug(f"UNIMENU: detected {dcc.name}")
            __import__(dcc.module)
            return dcc
    warnings.warn("UNIMENU: no supported DCC detected")
