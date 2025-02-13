from listener import Listener
from writer.console_log import ConsoleLog 
from writer.file_log import FileLog 
from parser.encryption.xor import Xor


def main():
    x = Xor()
    x.enc("dd")
    l = Listener()
    wr = ConsoleLog()
    wr2 = FileLog()
    l.start(wr.write, wr2.write)
    l.stop()
main()

