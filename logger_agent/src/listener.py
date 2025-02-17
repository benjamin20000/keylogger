from interface.listener_interface import ListenerInterface
import keyboard


class Listener(ListenerInterface):
    def __init__(self):
        super().__init__()
        self.buffer = []

    def get_buffer(self):
        temp_buffer = self.buffer
        self.buffer = []
        return temp_buffer
        
    def key_handler(self, key):
        self.buffer.append((key.name))

    def start(self):
        keyboard.on_press(self.key_handler)

    def stop(self):
        keyboard.wait('esc')


