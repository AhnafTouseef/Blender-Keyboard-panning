import os
import subprocess
import sys
from .config import *

# =========================================================================
#                               Function No.1
# =========================================================================

def launch_ahk_script():
    global ahk_process
    
    if sys.platform != "win32":
        print("AHK Numpad Panner: Not running on Windows. AHK script will not be launched.")
        return False

    addon_dir = os.path.dirname(__file__)
    ahk_script_path = os.path.join(addon_dir, AHK_COMPILED_FILENAME)

    if not os.path.exists(ahk_script_path):
        print(f"AHK Numpad Panner ERROR: Compiled AHK script not found at {ahk_script_path}")
        return False

    if ahk_process and ahk_process.poll() is None:
        print("AHK Numpad Panner: Script already running.")
        return True

    try:
        ahk_process = subprocess.Popen(
            [ahk_script_path],
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
        )
        print(f"AHK Numpad Panner: Launched script: {ahk_script_path} ")
        return True
    except Exception as e:
        print(f"AHK Numpad Panner ERROR: Failed to launch AHK script: {e}")
        ahk_process = None
        return False


# =========================================================================
#                               Function No.2
# =========================================================================

def terminate_ahk_script():
    global ahk_process
    if ahk_process and ahk_process.poll() is None:
        try:
            ahk_process.terminate()
            ahk_process.wait(timeout=2)
            if ahk_process.poll() is None:
                ahk_process.kill()
                print(f"AHK Numpad Panner: Force-killed script.")
            else:
                print(f"AHK Numpad Panner: Terminated script.")
        except Exception as e:
            print(f"AHK Numpad Panner ERROR: Failed to terminate AHK script: {e}")
    else:
         print("AHK Numpad Panner: Script was already stopped or finished.")
    ahk_process = None

addon_dir = os.path.dirname(__file__)
ahk_script_path = os.path.join(addon_dir, AHK_COMPILED_FILENAME)

print(f'The path is: {ahk_script_path}')


