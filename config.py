key_process = None

# --- Configuration (for add-on internal paths and filenames) ---
TEMPLATE_FILENAME = "template_blender_numpad_panner.ahk" # Source template for AHK script
GENERATED_FILENAME = "blender_numpad_panner_custom_keys.ahk" # Generated AHK script with custom keys
COMPILED_FILENAME = "blender_numpad_panner.exe" # Final compiled EXE (this is what is launched)

COMPILER_DIR_NAME = "compiler" # Subfolder name for compiler binaries
AHK_COMPILER_EXE = "Ahk2Exe.exe"   # Name of the compiler executable
AHK_COMPILER_BIN = "AutoHotkeySC.bin" # Name of the required compiler runtime binary


# --- Mapping from Blender's event.type tzo AutoHotkey key names ---
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
