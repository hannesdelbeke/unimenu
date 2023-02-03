"""
demo Maya plugin to setup a menu in maya on startup
"""

import maya.api.OpenMaya as om
import maya.utils
import traceback


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


# command
class MenuCmd(om.MPxCommand):
    kPluginCmdName = "UniMenu"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return MenuCmd()

    def doIt(self, args):
        raise Exception('Plugin not supposed to be invoked - only loaded & unloaded.')


# Initialize the plug-in
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin, "Hannes", "0.0.1", "Any")
    try:
        load()
    except:
        traceback.print_exc()
        raise


# Uninitialize the plug-in
def uninitializePlugin(plugin):
    # pluginFn = om.MFnPlugin(plugin)
    try:
        unload()
    except:
        traceback.print_exc()
        raise


def load():
    # If `load on startup' is enabled, this method runs before external modules are available,
    # resulting in errors. To fix this, the loading is done after Maya startup
    maya.utils.executeDeferred(load_deferred)


menu = None


def load_deferred():
    # since python modules are not available on startup
    # we defer any setup that needs unimenu until after startup

    import unimenu

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

    global menu
    menu = unimenu.setup_dict(config)
    # todo use new node class


def unload():
    import unimenu
    global menu
    unimenu.teardown_menu(menu)  # same name as top label in config
