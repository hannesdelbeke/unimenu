import unimenu
import pyblish_lite
import pathlib


icon_path = pathlib.Path(pyblish_lite.__file__).parent / "img" / "logo-extrasmall.png"
menu_node = unimenu.Node(
    label="pyblish lite",
    command="import pyblish_lite;pyblish_lite.show()",
    tooltip="Open Pyblish Lite",
    icon=str(icon_path),
)
menu_node.setup()
