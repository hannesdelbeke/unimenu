# openmenu
A pure python module to add python commands to the menu.

Supports unreal engine, blender, maya, krita, substance painter

<img src="samples/menu_screen_maya.jpg" width="400"/>
<img src="samples/menu_screen_unreal5.jpg" width="400"/>
<img src="samples/menu_screen_krita.jpg" width="400"/>
<img src="samples/menu_screen_substance_painter.jpg" width="400"/>

# how to use

create your config in yaml
```yaml
items:
  - name: my menu
    items:
      - name: my item
        command: print("Hello World")
```
or json
```json
{
   "name":"my menu",
   "items":[
      {
         "name":"my item",
         "command":"print(\"Hello World\")"
      },
      {
         "name":"my sub menu",
         "items":[
            {
               "name":"sub item 1",
               "command":"print(\"Hello World\")"
            }
         ]
      }
   ]
}     
```
run this to create your menu from the config
```python
import openmenu
openmenu.config_setup(config_path)
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

## Supports
- Unreal 5.0.2
- Blender 3.2, 2.93, 2.8 (minimum)
- Maya 2023, 2022 (minimum)

python 3.7+ due to f-strings and pathlib

## Alternatives
- Blender: [blender addon](https://github.com/friedererdmann/blender_menus)
- Blender: hacky way to create qt menu in blender - [shotgrid way](https://github.com/diegogarciahuerta/tk-blender/blob/d2c21fa53ab861886858388fbdc115e6d4e10a9d/resources/scripts/startup/Shotgun_menu.py#L156)
- Unreal: (paid) [python-toolbar-button-menu-creator](https://www.unrealengine.com/marketplace/en-US/product/python-toolbar-button-menu-creator/reviews?sessionInvalidated=true) and [docs](https://github.com/imgspc/UnrealMenuItem-Docs)

## Development

main platform is windows, would be interested to hear from mac & linux users.

feel free to create a PR to help out.

to add support for your favorite software, add a python module named after the software with a setup_menu function
