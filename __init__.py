bl_info = {
    "name": "Key panning",
    "author": "CG Explorer",
    "version": (1, 5),
    "blender": (3, 6, 0), 
    "location": "Add-ons Preferences",
    "description": "Launches an external AutoHotkey script for Numpad panning in Blender, with bundled compiler for key customization.",
    "warning": "This add-on requires a compiled AutoHotkey .exe script (Windows only). Recompilation is also Windows-only.",
    "category": "Interface",
}

import bpy
from .operators import *
from .preferences import *


classes = (
    BL_Key_Panning_Preferences,
    BL_OT_GenerateAndRecompileScript,
    BL_OT_ResetKeys,
    BL_OT_SetKeyModal,
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
