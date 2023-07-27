import os
import sys
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageOps

# Meta scroll switch workspace
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController

import threading

mouse = MouseController()
keyboard = KeyboardController()

# Hotkey - This is the global shortcut defined in the desktop environment settings
MODIFIERS: list = [Key.cmd, Key.ctrl]
HK_NEXT_WORKSPACE = Key.right
HK_PREVIOUS_WORKSPACE = Key.left

# Allows switching with scroll wheel
VERTICAL_SCROLLING: bool = True
HORIZONTAL_SCROLLING: bool = False
# TODO: Not implemented
INVERT_SCROLLING: bool = False

# App state
_enabled: bool = True
_meta_pressed: bool = False
_keys_pressed: set = set()

VSCROLL_UP = 1
VSCROLL_DOWN = -1
HSCROLL_LEFT = -1 
HSCROLL_RIGHT = 1

class MetaScrollerApp(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.keyboard_listener = None
        self.mouse_listener = None

    def on_press(self, key):
        if key not in [Key.cmd, Key.ctrl, Key.shift, Key.alt]:
            return
        _keys_pressed.add(key)

    def on_release(self, key):
        try:
            _keys_pressed.remove(key)
        except KeyError as e:
            pass

    def on_scroll(self, x, y, dx, dy):
        #print(_keys_pressed)
        # Make sure that only the Meta key is pressed, and no other modifier combination
        if len(_keys_pressed) != 1 or Key.cmd not in _keys_pressed:
            return
        hotkey = None
        if VERTICAL_SCROLLING and dy != 0:
            if dy == VSCROLL_UP:
                hotkey = HK_NEXT_WORKSPACE
            elif dy == VSCROLL_DOWN:
                hotkey = HK_PREVIOUS_WORKSPACE
        elif HORIZONTAL_SCROLLING and dx != 0:
            if dx == HSCROLL_LEFT:
                hotkey = HK_NEXT_WORKSPACE
            elif dx == HSCROLL_RIGHT:
                hotkey = HK_PREVIOUS_WORKSPACE
        if not hotkey:
            return
        # A bit messy, but handles pressing up to 3 modifier keys simultaneously
        if len(MODIFIERS) == 1:
            with keyboard.pressed(MODIFIERS[0]):
                keyboard.press(hotkey)
                keyboard.release(hotkey)
        elif len(MODIFIERS) == 2:
            with keyboard.pressed(MODIFIERS[0]):
                with keyboard.pressed(MODIFIERS[1]):
                    keyboard.press(hotkey)
                    keyboard.release(hotkey)
        elif len(MODIFIERS) == 3:
            with keyboard.pressed(MODIFIERS[0]):
                with keyboard.pressed(MODIFIERS[1]):
                    with keyboard.pressed(MODIFIERS[2]):
                        keyboard.press(hotkey)
                        keyboard.release(hotkey)

        #icon.notify('Switch workspace')
        keyboard.press(Key.cmd)

    def run(self):
        self.start_listening()

    def stop(self):
        self.keyboard_listener.stop()
        self.mouse_listener.stop()

    def start_listening(self):
        # Setup the listener threads
        self.keyboard_listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release)
        self.mouse_listener = MouseListener(on_scroll=self.on_scroll)
        # Start the threads and join them so the script doesn't end early
        self.keyboard_listener.start()
        self.mouse_listener.start()
        self.keyboard_listener.join()
        self.mouse_listener.join()

app = MetaScrollerApp()
icon_enabled = Image.open(os.path.join(sys.path[0], "metascroller-icon.png"))
icon_disabled = ImageOps.grayscale(icon_enabled)

enabled_state = True
def on_toggle_enabled(icon, item):
    global enabled_state
    global app
    enabled_state = not item.checked
    if item.checked:
        icon.icon = icon_enabled
        app = MetaScrollerApp()
        app.start()
    else:
        app.stop()
        app = None
        icon.icon = icon_disabled

def quit():
    app.stop()
    icon.stop()
    exit()

menu = (
    item(
        'Enabled',
        on_toggle_enabled,
        checked=lambda item: enabled_state),
    item('Quit MetaScroller', quit))
icon = pystray.Icon("name", icon_enabled, "Metascroller", menu)
app.daemon = True
app.start()
icon.run()