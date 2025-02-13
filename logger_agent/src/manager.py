from src.listener import Listener
from src.writer.console_log import ConsoleLog 
from src.writer.file_log import FileLog 
from src.parser.encryption.xor import Xor

def main():
    x = Xor()
    x.enc("dd")
    l = Listener()
    wr = ConsoleLog()
    wr2 = FileLog()
    l.start(wr.write, wr2.write)
    l.stop()
# main()

