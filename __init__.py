bl_info = {
    "name": "AHK Numpad Panner for Blender",
    "author": "Your Name / AI Assistant", # Feel free to put your name here!
    "version": (1, 5), # Increment version (e.g., to 1.5)
    "blender": (3, 6, 0), # Adjust to your minimum Blender version
    "location": "Add-ons Preferences",
    "description": "Launches an external AutoHotkey script for Numpad panning in Blender, with bundled compiler for key customization.",
    # "warning": "This add-on requires a compiled AutoHotkey .exe script (Windows only). Recompilation is also Windows-only.",
    "category": "Interface",
}

import bpy
from .operators import *
from .preferences import *


classes = (
    AHK_Numpad_Pan_Preferences,
    AHK_OT_GenerateAndRecompileScript,
    AHK_OT_ResetAHKKeys,
    AHK_OT_SetKeyModal,
)

def register():
    print("AHK Numpad Panner: Registering add-on...")
    for cls in classes:
        bpy.utils.register_class(cls)
    
    if bpy.context.preferences.addons.get(__name__):
        launch_ahk_script()
    print("AHK Numpad Panner: Add-on registered.")

def unregister():
    print("AHK Numpad Panner: Unregistering add-on...")
    terminate_ahk_script()
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("AHK Numpad Panner: Add-on unregistered.")
