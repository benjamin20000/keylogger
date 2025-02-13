import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from interface.writer_interface import WriterInterface


class Writer(WriterInterface):
    def write(self, message):
        print(message)
