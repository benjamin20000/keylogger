from src.listener import Listener
from src.writer.console_log import ConsoleLog 
from src.writer.file_log import FileLog 
from src.writer.json_log import JsonLog 
from src.parser.encryption.xor import Xor

from time import sleep
from threading import Thread


 
class manager:
    def __init__(self):
        self.l = Listener()
        self.wr = ConsoleLog()
        self.wr2 = FileLog()
        self.json = JsonLog()

    def write_buffer(self):
        while True:
            if self.l.buffer_has_data():
                buffer = self.l.get_buffer()
                # self.wr.write(buffer) ##write to consel
                # self.wr2.write(buffer) ##write to txt file
                str = "".join(buffer)
                self.json.write(str)
            sleep(5)   #TODO add the sleep time to config file  

    def main(self):
        ## write
        Thread(target=self.write_buffer, daemon=True).start()
        
        # Main program continues to do other things
        self.l.start()
        self.l.stop()


