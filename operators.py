import bpy, sys, subprocess, os
from .utils import *

# =========================================================================
#                               Operator No.1
# =========================================================================

class BL_OT_SetKeyModal(bpy.types.Operator):
    bl_idname = "bl.set_key_modal"
    bl_label = "Set Pan Key"
    bl_options = {'REGISTER', 'INTERNAL'}

    target_property: bpy.props.StringProperty(name="Target Property")
    target_label: bpy.props.StringProperty(name="Target Label")


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
            captured_key = KEY_MAP.get(event.type, None)
            
            if captured_key:
                # If a valid key name is found
                prefs = context.preferences.addons[__package__].preferences
                setattr(prefs, self.target_property, captured_key) # Update the preference property
                
                self.report({'INFO'}, f"Key '{captured_key}' assigned to '{self.target_label}'.")
                context.area.tag_redraw() # Force redraw to update UI
                return {'FINISHED'} # This implicitly removes the modal handler
            else:
                # If the pressed key is not in our KEY_MAP
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


# =========================================================================
#                               Operator No.2
# =========================================================================
    
# --- Generate and Recompile Operator Class (No changes) ---
class BL_OT_GenerateAndRecompileScript(bpy.types.Operator):
    bl_idname = "bl.generate_and_recompile_script"
    bl_label = "Generate & Recompile Script"
    bl_description = "Generates a new AHK script based on key preferences and recompiles it using the bundled compiler."

    @classmethod
    def poll(cls, context):
        return sys.platform == "win32"

    def execute(self, context):
        prefs = context.preferences.addons[__package__].preferences
        
        addon_dir = os.path.dirname(__file__)
        template_path = os.path.join(addon_dir, TEMPLATE_FILENAME)
        generated_path = os.path.join(addon_dir, GENERATED_FILENAME)
        compiled_exe_path = os.path.join(addon_dir, COMPILED_FILENAME)
        
        compiler_dir = os.path.join(addon_dir, COMPILER_DIR_NAME)
        compiler_exe_path = os.path.join(compiler_dir, COMPILER_EXE)
        compiler_bin_path = os.path.join(compiler_dir, COMPILER_BIN)

        if not os.path.exists(template_path):
            self.report({'ERROR'}, f"template script not found: '{TEMPLATE_FILENAME}'. Add-on might be corrupted.")
            return {'CANCELLED'}
        if not os.path.exists(compiler_exe_path) or not os.path.exists(compiler_bin_path):
            self.report({'ERROR'}, f"Bundled compiler files not found in '{COMPILER_DIR_NAME}'. Add-on might be corrupted or incomplete.")
            return {'CANCELLED'}

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
        except Exception as e:
            self.report({'ERROR'}, f"Failed to read template '{TEMPLATE_FILENAME}': {e}")
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
            with open(generated_path, 'w', encoding='utf-8') as f:
                f.write(generated_content)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to write generated script '{GENERATED_FILENAME}': {e}")
            return {'CANCELLED'}

        terminate_script()
        
        try:
            command = [
                compiler_exe_path,
                '/in', generated_path,
                '/out', compiled_exe_path,
                '/silent'
            ]
            
            print(f"Compile: Running command: {' '.join(command)}")
            process = subprocess.run(command, cwd=compiler_dir, capture_output=True, text=True, check=False)

            if process.returncode == 0:
                self.report({'INFO'}, f"Script generated and compiled successfully: {COMPILED_FILENAME}")
                launch_script()
                # Delete the generated script file after successful compilation
                try:
                    os.remove(generated_path)
                    print(f"Compile: Deleted temporary generated script '{generated_path}'")
                except Exception as e:
                    print(f"Compile: Failed to delete temporary script '{generated_path}': {e}")
            else:
                error_msg = f"Compilation failed (Error Code: {process.returncode})."
                if process.stdout:
                    error_msg += f"\nCompiler Output (stdout):\n{process.stdout}"
                if process.stderr:
                    error_msg += f"\nCompiler Errors (stderr):\n{process.stderr}"
                print(f"Compile ERROR: {error_msg}")
                self.report({'ERROR'}, "Compilation failed! Check Blender console for details.")

        except Exception as e:
            self.report({'ERROR'}, f"Error during Compilation process: {e}")
            print(f"Compile Exception: {e}")
        
        return {'FINISHED'}


# =========================================================================
#                               Operator No.3
# =========================================================================

# --- Reset Keys Operator Class (No changes) ---
class BL_OT_ResetKeys(bpy.types.Operator):
    bl_idname = "bl.reset_keys"
    bl_label = "Reset Keys"
    bl_description = "Resets key assignments to their default values (NumpadUp, NumpadDown, NumpadLeft, NumpadRight)."

    def execute(self, context):
        prefs = context.preferences.addons[__package__].preferences
        prefs.key_pan_up = "NumpadUp"
        prefs.key_pan_down = "NumpadDown"
        prefs.key_pan_left = "NumpadLeft"
        prefs.key_pan_right = "NumpadRight"
        self.report({'INFO'}, "Key assignments reset to defaults.")
        bpy.ops.bl.generate_and_recompile_script()
        return {'FINISHED'}
