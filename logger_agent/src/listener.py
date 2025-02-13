from interface.listener_interface import ListenerInterface
import keyboard


class Listener(ListenerInterface):
    def start(self, *arg):
        for key_handler in arg:
            keyboard.on_press(key_handler)

    def stop(self):
        keyboard.wait('esc')


