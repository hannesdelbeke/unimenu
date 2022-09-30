# maya_menu
A pure python helper module to add python commands to the maya menu.
![Menu screenshot](menu_screenshot.jpg)

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
run this to create your unreal menu from the config
```python
import maya_menu
maya_menu.setup(config_path)
```

## Notes
- support loading multiple configs. Great for a single studio config and several project configs. Or a team config.
- support creating another config to a previously created menu, or submenu!
