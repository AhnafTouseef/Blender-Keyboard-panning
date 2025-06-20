bl_info = {
    "name": "AHK Numpad Panner for Blender",
    "author": "Your Name / AI Assistant", # Feel free to put your name here!
    "version": (1, 5), # Increment version (e.g., to 1.5)
    "blender": (3, 6, 0), # Adjust to your minimum Blender version
    "location": "Add-ons Preferences",
    "description": "Launches an external AutoHotkey script for Numpad panning in Blender, with bundled compiler for key customization.",
    "warning": "This add-on requires a compiled AutoHotkey .exe script (Windows only). Recompilation is also Windows-only.",
    "category": "Interface",
}

import bpy
import subprocess
import os
import sys

# Global variable to store the Popen object for the AHK script process
ahk_process = None

# --- Configuration (for add-on internal paths and filenames) ---
AHK_TEMPLATE_FILENAME = "template_blender_numpad_panner.ahk" # Source template for AHK script
AHK_GENERATED_FILENAME = "blender_numpad_panner_custom_keys.ahk" # Generated AHK script with custom keys
AHK_COMPILED_FILENAME = "blender_numpad_panner.exe" # Final compiled EXE (this is what is launched)

AHK_COMPILER_DIR_NAME = "compiler" # Subfolder name for compiler binaries
AHK_COMPILER_EXE = "Ahk2Exe.exe"   # Name of the compiler executable
AHK_COMPILER_BIN = "AutoHotkeySC.bin" # Name of the required compiler runtime binary


# --- Mapping from Blender's event.type to AutoHotkey key names ---
# This dictionary translates Blender's internal key identifiers to names AHK understands.
# Refer to AutoHotkey's KeyList for more names: https://www.autohotkey.com/docs/v1/KeyList.htm
AHK_KEY_MAP = {
    # Alphanumeric (Blender's uppercase, AHK's lowercase for single letters)
    'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e', 'F': 'f', 'G': 'g', 'H': 'h', 'I': 'i', 'J': 'j',
    'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n', 'O': 'o', 'P': 'p', 'Q': 'q', 'R': 'r', 'S': 's', 'T': 't',
    'U': 'u', 'V': 'v', 'W': 'w', 'X': 'x', 'Y': 'y', 'Z': 'z',
    'ZERO': '0', 'ONE': '1', 'TWO': '2', 'THREE': '3', 'FOUR': '4', 'FIVE': '5', 'SIX': '6', 'SEVEN': '7', 'EIGHT': '8', 'NINE': '9',

    # Numpad
    'NUMPAD_0': 'Numpad0', 'NUMPAD_1': 'Numpad1', 'NUMPAD_2': 'Numpad2', 'NUMPAD_3': 'Numpad3',
    'NUMPAD_4': 'Numpad4', 'NUMPAD_5': 'Numpad5', 'NUMPAD_6': 'Numpad6', 'NUMPAD_7': 'Numpad7',
    'NUMPAD_8': 'Numpad8', 'NUMPAD_9': 'Numpad9',
    'NUMPAD_PERIOD': 'NumpadDot', 'NUMPAD_SLASH': 'NumpadDiv', 'NUMPAD_ASTERISK': 'NumpadMult',
    'NUMPAD_MINUS': 'NumpadSub', 'NUMPAD_PLUS': 'NumpadAdd', 'NUMPAD_ENTER': 'NumpadEnter',

    # Function Keys
    'F1': 'F1', 'F2': 'F2', 'F3': 'F3', 'F4': 'F4', 'F5': 'F5', 'F6': 'F6', 'F7': 'F7', 'F8': 'F8',
    'F9': 'F9', 'F10': 'F10', 'F11': 'F11', 'F12': 'F12',

    # Special Keys
    'SPACE': 'Space',
    'TAB': 'Tab',
    'RET': 'Enter', # RETURN in some contexts
    'INSERT': 'Ins',
    'DEL': 'Del',
    'HOME': 'Home',
    'END': 'End',
    'PAGE_UP': 'PgUp',
    'PAGE_DOWN': 'PgDn',
    'UP_ARROW': 'Up',
    'DOWN_ARROW': 'Down',
    'LEFT_ARROW': 'Left',
    'RIGHT_ARROW': 'Right',
    'BACK_SPACE': 'Backspace',
    'ESC': 'Escape',
    'CAPS_LOCK': 'CapsLock',
    'SCROLL_LOCK': 'ScrollLock',
    'PAUSE': 'Pause',

    # Modifiers (AutoHotkey can distinguish Left/Right versions)
    'LEFT_SHIFT': 'LShift', 'RIGHT_SHIFT': 'RShift',
    'LEFT_ALT': 'LAlt', 'RIGHT_ALT': 'RAlt',
    'LEFT_CTRL': 'LCtrl', 'RIGHT_CTRL': 'RCtrl',
    'OSKEY': 'LWin', # Windows key (OSKEY maps to Left Windows key)
    'APP_MENU': 'AppsKey', # Context Menu key

    # Mouse Buttons
    'LEFTMOUSE': 'LButton',
    'RIGHTMOUSE': 'RButton',
    'MIDDLEMOUSE': 'MButton',
    'MOUSE4': 'XButton1', # Side mouse button (often Button 4)
    'MOUSE5': 'XButton2', # Side mouse button (often Button 5)

    # Punctuation / Symbols (common ones, often match directly)
    'COMMA': ',',
    'PERIOD': '.',
    'SLASH': '/',
    'BACK_SLASH': '\\',
    'MINUS': '-',
    'EQUAL': '=',
    'LEFT_BRACKET': '[',
    'RIGHT_BRACKET': ']',
    'SEMI_COLON': ';',
    'QUOTE': "'",
    'ACCENT_GRAVE': '`', # Backtick
}

# --- Common Message Box Function ---
def show_delayed_message(message, title="AHK Numpad Panner"):
    """
    Schedules a message box to be shown after a short delay.
    This avoids context errors during add-on registration.
    """
    def _inner_show():
        try:
            bpy.ops.wm.show_message_box(
                'INVOKE_DEFAULT',
                title=title,
                message=message
            )
        except Exception as e:
            print(f"AHK Numpad Panner: Failed to show message box: {e}")
        return None
    bpy.app.timers.register(_inner_show, first_interval=0.1)


# --- AHK Script Management Functions (No changes here) ---
def launch_ahk_script():
    global ahk_process
    
    if sys.platform != "win32":
        print("AHK Numpad Panner: Not running on Windows. AHK script will not be launched.")
        show_delayed_message("Not running on Windows. AHK script will not be launched.", title="Platform Warning")
        return False

    addon_dir = os.path.dirname(__file__)
    ahk_script_path = os.path.join(addon_dir, AHK_COMPILED_FILENAME)

    if not os.path.exists(ahk_script_path):
        print(f"AHK Numpad Panner ERROR: Compiled AHK script not found at {ahk_script_path}")
        show_delayed_message(
            f"Compiled AHK script '{AHK_COMPILED_FILENAME}' not found in add-on folder. "
            "Please use the 'Generate & Recompile AHK Script' button in preferences.",
            title="AHK Numpad Panner Error"
        )
        return False

    if ahk_process and ahk_process.poll() is None:
        print("AHK Numpad Panner: Script already running.")
        return True

    try:
        ahk_process = subprocess.Popen(
            [ahk_script_path],
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
        )
        print(f"AHK Numpad Panner: Launched script: {ahk_script_path} (PID: {ahk_process.pid})")
        show_delayed_message("AHK script launched successfully! Use your custom Numpad keys for panning.", title="AHK Numpad Panner")
        return True
    except Exception as e:
        print(f"AHK Numpad Panner ERROR: Failed to launch AHK script: {e}")
        ahk_process = None
        show_delayed_message(f"Failed to launch AHK script: {e}. Check console for details.", title="AHK Numpad Panner Error")
        return False

def terminate_ahk_script():
    global ahk_process
    if ahk_process:
        if ahk_process.poll() is None:
            try:
                ahk_process.terminate()
                ahk_process.wait(timeout=2)
                if ahk_process.poll() is None:
                    ahk_process.kill()
                    print(f"AHK Numpad Panner: Force-killed script (PID: {ahk_process.pid}).")
                else:
                    print(f"AHK Numpad Panner: Terminated script (PID: {ahk_process.pid}).")
            except Exception as e:
                print(f"AHK Numpad Panner ERROR: Failed to terminate AHK script: {e}")
        else:
            print("AHK Numpad Panner: Script was already stopped or finished.")
        ahk_process = None


# --- Addon Preferences Class (UI updated for Set Key buttons) ---
class AHK_Numpad_Pan_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    key_pan_up: bpy.props.StringProperty(
        name="Pan Up Key",
        description="Key to pan the view up (e.g., 'NumpadUp', 'W', 'Space', 'LButton').",
        default="NumpadUp",
    )
    key_pan_down: bpy.props.StringProperty(
        name="Pan Down Key",
        description="Key to pan the view down (e.g., 'NumpadDown', 'S').",
        default="NumpadDown",
    )
    key_pan_left: bpy.props.StringProperty(
        name="Pan Left Key",
        description="Key to pan the view left (e.g., 'NumpadLeft', 'A').",
        default="NumpadLeft",
    )
    key_pan_right: bpy.props.StringProperty(
        name="Pan Right Key",
        description="Key to pan the view right (e.g., 'NumpadRight', 'D').",
        default="NumpadRight",
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Customize AHK Panning Hotkeys (Windows Only)", icon='FILE_SCRIPT')
        
        # UI for Pan Up Key
        row = box.row(align=True)
        row.prop(self, "key_pan_up")
        op = row.operator("ahk.set_key_modal", text="Set Key")
        op.target_property = "key_pan_up"
        op.target_label = "Pan Up Key" # Pass label for better modal feedback

        # UI for Pan Down Key
        row = box.row(align=True)
        row.prop(self, "key_pan_down")
        op = row.operator("ahk.set_key_modal", text="Set Key")
        op.target_property = "key_pan_down"
        op.target_label = "Pan Down Key"

        # UI for Pan Left Key
        row = box.row(align=True)
        row.prop(self, "key_pan_left")
        op = row.operator("ahk.set_key_modal", text="Set Key")
        op.target_property = "key_pan_left"
        op.target_label = "Pan Left Key"

        # UI for Pan Right Key
        row = box.row(align=True)
        row.prop(self, "key_pan_right")
        op = row.operator("ahk.set_key_modal", text="Set Key")
        op.target_property = "key_pan_right"
        op.target_label = "Pan Right Key"

        row = box.row(align=True)
        row.operator("ahk.generate_and_recompile_script", icon='FILE_REFRESH', text="Generate & Recompile AHK Script")
        row.operator("ahk.reset_ahk_keys", text="Reset Keys", icon='FILE_DELETED')

        box.separator()
        box.label(text="Important Notes:")
        box.label(text="- Use the 'Set Key' button to press your desired key.")
        row_template = box.row(align=True)
        row_template.label(text="- Other settings (speed, acceleration) can be edited in:")
        row_template.operator("wm.url_open", text=AHK_TEMPLATE_FILENAME, icon='FILE_SCRIPT').url = \
            "file://" + os.path.join(os.path.dirname(__file__), AHK_TEMPLATE_FILENAME).replace("\\", "/")

        box.label(text="- The generated script will be '%s' and compiled to '%s'." % (AHK_GENERATED_FILENAME, AHK_COMPILED_FILENAME))


# --- Modal Operator for Setting Keys by Pressing Them (MODIFIED) ---
class AHK_OT_SetKeyModal(bpy.types.Operator):
    bl_idname = "ahk.set_key_modal"
    bl_label = "Set Pan Key"
    bl_options = {'REGISTER', 'INTERNAL'}

    target_property: bpy.props.StringProperty(name="Target Property")
    target_label: bpy.props.StringProperty(name="Target Label")

    _timer = None # For potential future use (e.g., timeout)

    @classmethod
    def poll(cls, context):
        return sys.platform == "win32"

    def invoke(self, context, event):
        if context.window_manager.modal_handler_add(self):
            self.report({'INFO'}, f"Press a key for '{self.target_label}'... (Press ESC to cancel)")
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Modal operator failed to start.")
            return {'CANCELLED'}

    def modal(self, context, event):
        # Allow ESC key to cancel the modal
        if event.type == 'ESC' and event.value == 'PRESS':
            self.report({'CANCELLED'}, f"Key assignment for '{self.target_label}' cancelled.")
            context.area.tag_redraw()
            return {'CANCELLED'} # This implicitly removes the modal handler

        # Only process key down or mouse button press events
        if event.value == 'PRESS':
            captured_key_ahk = AHK_KEY_MAP.get(event.type, None)
            
            if captured_key_ahk:
                # If a valid AHK key name is found
                prefs = context.preferences.addons[__name__].preferences
                setattr(prefs, self.target_property, captured_key_ahk) # Update the preference property
                
                self.report({'INFO'}, f"Key '{captured_key_ahk}' assigned to '{self.target_label}'.")
                context.area.tag_redraw() # Force redraw to update UI
                return {'FINISHED'} # This implicitly removes the modal handler
            else:
                # If the pressed key is not in our AHK_KEY_MAP
                self.report({'WARNING'}, f"Unsupported key '{event.type}'. Please try another key. (Press ESC to cancel)")
                return {'RUNNING_MODAL'} # Keep listening

        return {'PASS_THROUGH'} # Allow other events to pass through to Blender (less disruptive)

    def cancel(self, context):
        # This method is called if modal_handler_remove was *explicitly* called elsewhere,
        # or if the user cancels via ESC, we return {'CANCELLED'} which calls this indirectly.
        # Since we removed modal_handler_remove, this cancel method acts as a cleanup.
        self.report({'CANCELLED'}, f"Key assignment for '{self.target_label}' cancelled.")
        context.area.tag_redraw()
        return {'CANCELLED'} # Ensure this always returns a final status


# --- Generate and Recompile Operator Class (No changes) ---
class AHK_OT_GenerateAndRecompileScript(bpy.types.Operator):
    bl_idname = "ahk.generate_and_recompile_script"
    bl_label = "Generate & Recompile AHK Script"
    bl_description = "Generates a new AHK script based on key preferences and recompiles it using the bundled compiler."

    @classmethod
    def poll(cls, context):
        return sys.platform == "win32"

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        
        addon_dir = os.path.dirname(__file__)
        template_path = os.path.join(addon_dir, AHK_TEMPLATE_FILENAME)
        generated_ahk_path = os.path.join(addon_dir, AHK_GENERATED_FILENAME)
        compiled_exe_path = os.path.join(addon_dir, AHK_COMPILED_FILENAME)
        
        compiler_dir = os.path.join(addon_dir, AHK_COMPILER_DIR_NAME)
        compiler_exe_path = os.path.join(compiler_dir, AHK_COMPILER_EXE)
        compiler_bin_path = os.path.join(compiler_dir, AHK_COMPILER_BIN)

        if not os.path.exists(template_path):
            self.report({'ERROR'}, f"AHK template script not found: '{AHK_TEMPLATE_FILENAME}'. Add-on might be corrupted.")
            return {'CANCELLED'}
        if not os.path.exists(compiler_exe_path) or not os.path.exists(compiler_bin_path):
            self.report({'ERROR'}, f"Bundled compiler files not found in '{AHK_COMPILER_DIR_NAME}'. Add-on might be corrupted or incomplete.")
            return {'CANCELLED'}

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
        except Exception as e:
            self.report({'ERROR'}, f"Failed to read AHK template '{AHK_TEMPLATE_FILENAME}': {e}")
            return {'CANCELLED'}

        replacements = {
            "%%HOTKEY_UP%%": prefs.key_pan_up,
            "%%HOTKEY_DOWN%%": prefs.key_pan_down,
            "%%HOTKEY_LEFT%%": prefs.key_pan_left,
            "%%HOTKEY_RIGHT%%": prefs.key_pan_right,
        }

        generated_content = template_content
        for placeholder, key in replacements.items():
            generated_content = generated_content.replace(placeholder, str(key))

        try:
            with open(generated_ahk_path, 'w', encoding='utf-8') as f:
                f.write(generated_content)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to write generated AHK script '{AHK_GENERATED_FILENAME}': {e}")
            return {'CANCELLED'}

        terminate_ahk_script()
        
        try:
            command = [
                compiler_exe_path,
                '/in', generated_ahk_path,
                '/out', compiled_exe_path,
                '/silent'
            ]
            
            print(f"AHK Compile: Running command: {' '.join(command)}")
            process = subprocess.run(command, cwd=compiler_dir, capture_output=True, text=True, check=False)

            if process.returncode == 0:
                self.report({'INFO'}, f"AHK script generated and compiled successfully: {AHK_COMPILED_FILENAME}")
                show_delayed_message(f"AHK script generated and compiled successfully! ({AHK_COMPILED_FILENAME})", title="Compilation Success")
                launch_ahk_script()
            else:
                error_msg = f"AHK compilation failed (Error Code: {process.returncode})."
                if process.stdout:
                    error_msg += f"\nCompiler Output (stdout):\n{process.stdout}"
                if process.stderr:
                    error_msg += f"\nCompiler Errors (stderr):\n{process.stderr}"
                print(f"AHK Compile ERROR: {error_msg}")
                self.report({'ERROR'}, "AHK compilation failed! Check Blender console for details.")
                show_delayed_message("AHK compilation failed! See console for details.", title="Compilation Failed")

        except Exception as e:
            self.report({'ERROR'}, f"Error during AHK compilation process: {e}")
            print(f"AHK Compile Exception: {e}")
            show_delayed_message(f"Error during AHK compilation process: {e}", title="Compilation Error")
        
        return {'FINISHED'}


# --- Reset Keys Operator Class (No changes) ---
class AHK_OT_ResetAHKKeys(bpy.types.Operator):
    bl_idname = "ahk.reset_ahk_keys"
    bl_label = "Reset Keys"
    bl_description = "Resets key assignments to their default values (NumpadUp, NumpadDown, NumpadLeft, NumpadRight)."

    def execute(self, context):
        prefs = context.preferences.addons[__name__].preferences
        prefs.key_pan_up = "NumpadUp"
        prefs.key_pan_down = "NumpadDown"
        prefs.key_pan_left = "NumpadLeft"
        prefs.key_pan_right = "NumpadRight"
        self.report({'INFO'}, "Key assignments reset to defaults.")
        return {'FINISHED'}


# =========================================================================
#                       BLENDER ADD-ON REGISTRATION
# =========================================================================

# List of all classes to register/unregister
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

if __name__ == "__main__":
    register()
