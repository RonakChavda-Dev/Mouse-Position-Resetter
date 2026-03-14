'''

TODO:
*1. Track mouse pointer position asyc. 
*2. Listen for event of still mouse position
*3. Save the idle mouse location
*4. Listen of hotkey asyc.
5. Change mouse pointer position to saved location on press of hotkey
6. Add Esc program close mechanism

'''

from difflib import restore
from pynput import mouse, keyboard
import time
import threading
import os


last_shift_time = time.time()
saved_position = None
mouse_controller = mouse.Controller()
current_keystroke = set()

def restore_cursor_position():
    if saved_position:
        mouse_controller.position = saved_position
        print("Last Saved Position Restored!")
    else:
        print("No Saved Position Availble.")

def move_alert(x, y):
    global last_shift_time
    last_shift_time = time.time()
    # print(f"Mouse position moved at {x}, {y}")


def mouse_inactivity_detector():
    global saved_position
    global mouse_controller

    while True:
        time.sleep(1)

        inactivity_time = time.time() - last_shift_time

        if inactivity_time >=5:
            saved_position = mouse_controller.position
            print(f"Restore point saved at {saved_position}")


def on_key_press(key):
    current_keystroke.add(key)
    print(current_keystroke)

    if keyboard.Key.ctrl_l in current_keystroke and keyboard.Key.alt_l in current_keystroke and keyboard.Key.f1 in current_keystroke:
        print("Mouse pointer position reset request recieved!")
        print("Initiating restore process...")
        restore_cursor_position()


def on_key_release(key):
    current_keystroke.remove(key)

    if key == keyboard.Key.esc:
        print("Exiting Program...")
        os._exit(0)
    


monitoring_thread = threading.Thread(target=mouse_inactivity_detector, daemon=True)
monitoring_thread.start()

mouse_event_listener = mouse.Listener(on_move=move_alert)
mouse_event_listener.start()

keyboard_event_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
keyboard_event_listener.start()


mouse_event_listener.join()
keyboard_event_listener.join()


