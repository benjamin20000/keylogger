from interface.writer_interface import WriterInterface


class ConsoleLog(WriterInterface):
    def write(self, buffer):
        for key in buffer:
            print(key)