import os, subprocess, sys
from .config import *

# =========================================================================
#                               Function No.1
# =========================================================================

def launch_script():
    global key_process
    
    if sys.platform != "win32":
        print("Key panning: Not running on Windows. script will not be launched.")
        return False

    addon_dir = os.path.dirname(__file__)
    script_path = os.path.join(addon_dir, COMPILED_FILENAME)

    if not os.path.exists(script_path):
        print(f"Key panning ERROR: Compiled script not found at {script_path}")
        return False

    if key_process and key_process.poll() is None:
        print("Key panning: Script already running.")
        return True

    try:
        key_process = subprocess.Popen(
            [script_path],
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
        )
        print(f"Key panning: Launched script: {script_path} ")
        return True
    except Exception as e:
        print(f"Key panning ERROR: Failed to launch script: {e}")
        key_process = None
        return False


# =========================================================================
#                               Function No.2
# =========================================================================

def terminate_script():
    global key_process
    if key_process and key_process.poll() is None:
        try:
            key_process.terminate()
            key_process.wait(timeout=2)
            if key_process.poll() is None:
                key_process.kill()
                print(f"Key panning: Force-killed script.")
            else:
                print(f"Key panning: Terminated script.")
        except Exception as e:
            print(f"Key panning ERROR: Failed to terminate script: {e}")
    else:
         print("Key panning: Script was already stopped or finished.")
    key_process = None
