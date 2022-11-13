"""
This submodule contains the dcc-specific implementations of the menu setup.
"""

import warnings
from collections import namedtuple
import contextlib
from typing import Optional


# name: the name of the dcc, and also the name of the menu module
# name of module: a unique python module only available in that dcc
# callback: not sure if we need this
DCC = namedtuple('DCC', ['name', 'module'])


class SupportedDCCs:
    """DCCs supported by this module"""

    # dcc -> digital content creation (software)

    BLENDER = DCC('blender', 'bpy')
    MAYA = DCC('maya', 'maya')  # pymel can be slow to import
    UNREAL = DCC('unreal', 'unreal')
    MAX = DCC('max', 'pymxs')
    KRITA = DCC('krita', 'krita')
    SUBSTANCE_DESIGNER = DCC('substance_designer', 'pysbs')
    SUBSTANCE_PAINTER = DCC('substance_painter', 'substance_painter')
    MARMOSET = DCC('marmoset', 'mset')

    ALL = [BLENDER, MAYA, UNREAL, KRITA, SUBSTANCE_PAINTER, MAX, MARMOSET]


def detect_dcc() -> Optional[DCC]:
    """detect which dcc is currently running"""
    for dcc in SupportedDCCs.ALL:
        with contextlib.suppress(ImportError):
            __import__(dcc.module)
            print(f"OPENMENU: detected {dcc.name}")
            return dcc
    warnings.warn("OPENMENU: no supported DCC detected")