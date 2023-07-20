'''
    Adds Context menus to assets in the browser.
    to specify an asset context use the asset type as parent_path.

    full list of ui names here https://dev.epicgames.com/community/snippets/exo/unreal-engine-editor-ui-menu-names

    and the kwarg context_menu on the root noode

'''

import unreal
import unimenu


def test_function():
    selected = unreal.EditorUtilityLibrary.get_selected_assets()
    unreal.AssetEditorSubsystem().open_editor_for_assets(selected)


config = {
    'label': 'StaticMesh Tools',
    'parent_path': "ContentBrowser.AssetContextMenu.StaticMesh",
    'kwargs': {
        "menu_section": "GetAssetActions"
                },

    'items':

        [
            {
                'command': 'test_function()',
                'label': 'Open Selected Asset',
                "icon": "MessageLog.TabIcon",
                "tooltip": "tooltip",

            },
            {
                'label': 'label',
                'separator': True,
                "icon": "BlueprintEditor.AddNewFunction",
                "tooltip": "tooltip separator",

            },
            {
                'command': 'print("hello 2")',
                'label': 'tool2',
                'icon': "BlueprintEditor.AddNewEventGraph"

            },
            {
                'label': 'Tools',

                'items':
                    [
                        {
                            'command': 'print("hello 1")',
                            'label': 'tool1',
                            'icon': "MessageLog.TabIcon"
                        },
                        {
                            'command': 'print("hello 2")',
                            'label': 'tool2',
                            'icon': "MessageLog.TabIcon"
                        }
                    ]
            }
        ]
}

# test teardown
node = unimenu.setup(config, backlink=False)
