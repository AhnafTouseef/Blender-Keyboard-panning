bl_info = {
    "name": "Numpad Panner",
    "author": "Your AI Assistant",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "Blender UI",
    "description": "Launches an external AutoHotkey script for Numpad panning in Blender.",
    "warning": "This add-on requires a compiled AutoHotkey script (Windows only).",
    "category": "Interface",
}

import bpy
import subprocess
import os
import sys

# Global variable to store the Popen object for the AHK script process
# This allows us to launch and later terminate the script.
ahk_process = None

# --- Configuration ---

AHK_SCRIPT_FILENAME = "blender_numpad_panner.exe" 

def show_delayed_message(message, title="Numpad Panner"):
    """
    Schedules a message box to be shown after a short delay.
    This avoids context errors during add-on registration.
    """
    def _inner_show():
        # This function runs when the timer fires, guaranteeing a proper context
        try:
            bpy.ops.wm.show_message_box(
                'INVOKE_DEFAULT',
                title=title,
                message=message
            )
        except Exception as e:
            print(f"Numpad Panner: Failed to show message box: {e}")
        return None # Return None to unregister the timer after it runs once

    # Register a timer to call _inner_show after 0.1 seconds
    bpy.app.timers.register(_inner_show, first_interval=0.1)


def launch_ahk_script():
    global ahk_process

    # Check if running on Windows, as AHK is Windows-specific
    if sys.platform != "win32":
        print("Numpad Panner: Not running on Windows. compiled script will not be launched.")
        show_delayed_message("Not running on Windows. compiled script will not be launched.", title="Platform Warning")
        return False # Indicate failure

    # Get the path to the current add-on directory
    addon_dir = os.path.dirname(__file__)
    ahk_script_path = os.path.join(addon_dir, AHK_SCRIPT_FILENAME)

    if not os.path.exists(ahk_script_path):
        print(f"Numpad Panner ERROR: script not found at {ahk_script_path}")
        show_delayed_message(f"script not found! Place '{AHK_SCRIPT_FILENAME}' in add-on folder.", title="Numpad Panner Error")
        return False # Indicate failure

    # Check if the process is already running or if it's a zombie process
    if ahk_process and ahk_process.poll() is None: # poll() returns None if process is running
        print("AHK Numpad Panner: Script already running.")
        # No message box here, as it might be annoying if re-enabled repeatedly
        return True # Indicate success, as script is already running

    try:
        # Launch the AHK script as a detached process
        # creationflags=subprocess.DETACHED_PROCESS prevents it from being killed if Blender crashes
        # Also ensures it doesn't open a console window if compiled with Gui-less option
        ahk_process = subprocess.Popen([ahk_script_path], creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW)
        print(f"AHK Numpad Panner: Launched script: {ahk_script_path} (PID: {ahk_process.pid})")
        show_delayed_message("AHK script launched successfully! Use Numpad for panning.", title="AHK Numpad Panner")
        return True # Indicate success
    except Exception as e:
        print(f"AHK Numpad Panner ERROR: Failed to launch AHK script: {e}")
        ahk_process = None # Clear process object if launch failed
        show_delayed_message(f"Failed to launch AHK script: {e}. Check console for details.", title="AHK Numpad Panner Error")
        return False # Indicate failure

def terminate_ahk_script():
    global ahk_process
    if ahk_process:
        if ahk_process.poll() is None: # Check if the process is still running
            try:
                # Terminate the process gently, then kill if needed
                ahk_process.terminate()
                ahk_process.wait(timeout=2) # Give it 2 seconds to terminate
                if ahk_process.poll() is None: # If still running, force kill
                    ahk_process.kill()
                    print(f"AHK Numpad Panner: Force-killed script (PID: {ahk_process.pid}).")
                else:
                    print(f"AHK Numpad Panner: Terminated script (PID: {ahk_process.pid}).")
            except Exception as e:
                print(f"AHK Numpad Panner ERROR: Failed to terminate AHK script: {e}")
        else:
            print("AHK Numpad Panner: Script was already stopped or finished.")
        ahk_process = None # Clear the reference

def register():
    # This function is called when the add-on is enabled
    print("AHK Numpad Panner: Registering add-on...")
    launch_ahk_script() # This function now handles its own message scheduling
    print("AHK Numpad Panner: Add-on registered.")

def unregister():
    # This function is called when the add-on is disabled or Blender exits
    print("AHK Numpad Panner: Unregistering add-on...")
    terminate_ahk_script()
    print("AHK Numpad Panner: Add-on unregistered.")

if __name__ == "__main__":
    register()