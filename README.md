# openmenu
A pure python module to add python commands to the menu.

Supports Unreal Engine, Blender, Maya, Krita, Substance Painter, 3ds Max, Marmoset

<img src="samples/menu_screen_maya.jpg" width="400"/> <img src="samples/menu_screen_unreal5.jpg" width="400"/> <img src="samples/menu_screen_krita.jpg" width="400"/> <img src="samples/menu_screen_substance_painter.jpg" width="400"/>

# how to use

you can make your menu(s):
- from a config
- from a dict
- with explicit code
- from a folder of scripts

### load from config (YAML & JSON)
```yaml
items:
  - name: my menu
    items:
      - name: my item
        command: print("Hello World")
```
```python
import openmenu
openmenu.setup_config(config_path)
```

### load from dynamic dict 

```python
import openmenu
data = {"items": [{"label": test,"command": 'print("hello world")'}]}
openmenu.setup_dict(data)
```


### with code

```python
import openmenu
openmenu.add_item(label="my submenu")  # create a submenu, parent defaults to the menu bar
openmenu.add_item(label="hello", command='print("hello world")', parent="OPENMENU_MT_my_submenu")  # add menu item to our submenu
```

### from a folder of scripts (module)

great for a folder full of tools that need launching when clicking a button.
1. ensure the folder is importable (in the sys.path)
2. create a menthod in all submodules with the same name, e.g. def show()
```python
import openmenu
openmenu.module_setup('name_of_folder', function_name='show', menu_name="My tools")
```


## When to use

some software e.g. Unity & Maya already have good ways to make custom menus. If you only use 1 software and find it easy to make a menu, you don't need openmenu.

The power of this module comes from standardising menu creation across multiple software. Great for studio-pipelines with several programs.
Openmenu can also help to make menu creation less complex e.g. in Blender.

## Notes
- support loading multiple configs. Great for a single studio config and several project configs. Or a team config.
- support creating another config to a previously created menu, or submenu!

Unreal
- load on startup with [init_unreal.py](https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/ScriptingAndAutomation/Python/#theinit_unreal.pyfile)

Blender
- load on startup with a script in the [startup folder](https://docs.blender.org/manual/en/dev/advanced/blender_directory_layout.html#path-layout)
- support blender icons in menu (see [sample yaml](https://github.com/hannesdelbeke/openmenu/blob/main/samples/menu_config_blender.yaml))

Krita
- native PyQt5
- print doesn't print to console

Substance Painter
- native PySide2
- print doesn't print to console

3ds Max
- native PySide2

Marmoset
- doesn't support menu extension, so we create a window with buttons instead
- run a script on startup with command line arguments: "toolbag.exe" "script-path" (not tested yet)

## Supports
openmenu was tested in the following versions, and might work in other versions.
- Unreal 5.0.2
- Blender 3.2, 2.93, 2.8 (minimum)
- Maya 2023, 2022 (minimum)
- Substance Painter 8.2.0
- Max 2024
- Marmoset 3.08

python 3.7+ due to f-strings and pathlib

## Alternatives
- Blender: [blender addon](https://github.com/friedererdmann/blender_menus), hacky way to create qt menu in blender: [shotgrid way](https://github.com/diegogarciahuerta/tk-blender/blob/d2c21fa53ab861886858388fbdc115e6d4e10a9d/resources/scripts/startup/Shotgun_menu.py#L156)
- Unreal: (paid) [python-toolbar-button-menu-creator](https://www.unrealengine.com/marketplace/en-US/product/python-toolbar-button-menu-creator/reviews?sessionInvalidated=true) and [docs](https://github.com/imgspc/UnrealMenuItem-Docs)
- https://github.com/Colorbleed/scriptsmenu
- Max: [default menu system](https://help.autodesk.com/view/3DSMAX/2017/ENU/?guid=GUID-90D08333-ADB3-4E8C-9579-1A0A71985604)
- After effects: (paid) [kbar](https://aescripts.com/kbar/)

## Development

main platform is windows, would be interested to hear from mac & linux users.

feel free to create a PR to help out.

to add support for your favorite software, add a python module named after the software with a setup_menu function
where possible stick to the windows menu [design guidelines](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/bb226797(v=vs.85))
