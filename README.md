# openmenu
A pure python module to add python commands to the menu.

Supports unreal engine, blender, maya

![Menu screenshot](samples/menu_screen_maya.jpg)

![Menu screenshot](samples/menu_screen_unreal5.jpg)


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

## Notes
- support loading multiple configs. Great for a single studio config and several project configs. Or a team config.
- support creating another config to a previously created menu, or submenu!

Unreal
- load on startup with [init_unreal.py](https://docs.unrealengine.com/4.27/en-US/ProductionPipelines/ScriptingAndAutomation/Python/#theinit_unreal.pyfile)

Blender
- load on startup with a script in the startup folder
- support blender icons in menu (see [sample yaml](https://github.com/hannesdelbeke/openmenu/blob/main/samples/menu_config_blender.yaml))

## Supports
- Unreal 5.0.2
- Blender 3.2, 2.93, 2.8 (minimum)
- Maya 2023, 2022 (minimum)

python 3.7+ due to f-strings and pathlib
