from interface.writer_interface import WriterInterface
from datetime import datetime

class FileLog(WriterInterface):
    def __init__(self):
        super().__init__()
        self.time_stamp = datetime.now()
        self.words_per_line = 10
        self.words_count = 0

    def write(self, message):
        with open("log_file", "a") as f:
            if self.words_per_line <= self.words_count:
                f.write("\n")
                self.words_count = 0
            
            if (datetime.now() - self.time_stamp).total_seconds()//60 > 1:
                f.write(f"\n ===={datetime.now()}====\n")
                self.time_stamp = datetime.now()


            self.words_count +=1
            f.write(str(message.name))

