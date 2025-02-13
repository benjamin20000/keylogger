import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from interface.writer_interface import WriterInterface


class FileLog(WriterInterface):
    def write(self, message):
        with open("log_file", "a") as f:
            f.write(str(message.name))