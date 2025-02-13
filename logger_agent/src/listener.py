import keyboard
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from interface.listener_interface import ListenerInterface


class Listener(ListenerInterface):
    def start(self, *arg):
        for key_handler in arg:
            keyboard.on_press(key_handler)

    def stop(self):
        keyboard.wait('esc')


