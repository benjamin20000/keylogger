from interface.writer_interface import WriterInterface


class ConsoleLog(WriterInterface):
    def write(self, message):
        print(message.name)