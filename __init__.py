bl_info = {
    "name": "Key panning",
    "author": "CG Explorer",
    "version": (1, 5),
    "blender": (3, 6, 0), 
    "location": "Add-ons Preferences",
    "description": "Launches an external AutoHotkey script for keyboard panning in Blender, with bundled compiler for key customization.",
    "category": "Interface",
    "warning": "This add-on requires a compiled AutoHotkey .exe script (Windows only). Recompilation is also Windows-only.",
}

import bpy
from .operators import *
from .preferences import *

classes = (
    BL_KEY_Pan_Preferences,
    BL_KEY_GenerateAndRecompileScript,
    BL_KEY_ResetKeys,
    BL_KEY_SetKeyModal,
    BL_KEY_OpenTemplateFile
)

def register():
    print("Key panning: Registering add-on...")
    for cls in classes:
        bpy.utils.register_class(cls)
    
    if bpy.context.preferences.addons.get(__name__):
        launch_script()
    print("Key panning: Add-on registered.")


def unregister():
    print("Key panning: Unregistering add-on...")
    terminate_script()
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("Key panning: Add-on unregistered.")
