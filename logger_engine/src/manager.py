from listener import Listener
from write import Writer



def main():
    l = Listener()
    wr = Writer()
    wr.write("hhh")
    l.start(wr.write)
    l.stop()
main()

