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
    'label': 'Context Tools',
    'parent_path': "StaticMesh",
    'context_menu': True,

    'items':

        [
            {
                'command': 'test_function()',
                'label': 'Open Selected Asset',
                "icon": ":/qt-project.org/styles/commonstyle/images/up-32.png",
                "tooltip": "tooltip",

            },
            {
                'label': 'label',
                'separator': True,
                "icon": ":/qt-project.org/styles/commonstyle/images/up-32.png",
                "tooltip": "tooltip separator",

            },
            {
                'command': 'print("hello 2")',
                'label': 'tool2',

            },
            {
                'label': 'Tools',

                'items':
                    [
                        {
                            'command': 'print("hello 1")',
                            'label': 'tool1'
                        },
                        {
                            'command': 'print("hello 2")',
                            'label': 'tool2'
                        }
                    ]
            }
        ]
}

# test teardown
node = unimenu.load(config)
app_node = node.setup(backlink=False)
