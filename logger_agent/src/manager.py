from src.listener import Listener
from src.writer.console_log import ConsoleLog 
from src.writer.file_log import FileLog 
from src.parser.encryption.xor import Xor

from time import sleep
from threading import Thread


 
class manager:
    def __init__(self):
        self.l = Listener()
        self.wr = ConsoleLog()
        self.wr2 = FileLog()

    def write_buffer(self):
        while True:
            if self.l.buffer_has_data():
                buffer = self.l.get_buffer()
                self.wr.write(buffer)
                self.wr2.write(buffer)
            sleep(5)   #TODO add the sleep time to config file  

    def main(self):
        ## write
        Thread(target=self.write_buffer, daemon=True).start()
        
        # Main program continues to do other things
        self.l.start()
        self.l.stop()


