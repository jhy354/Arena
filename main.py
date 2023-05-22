import sys
import getopt

from game import Game

usage = "usage: python server.py [-a | --address]"

if __name__ == "__main__":

    argv = sys.argv
    opts = None
    args = None
    server_ip = None

    try:
        opts, args = getopt.getopt(argv[1:], "-a:", ["address="])
    except getopt.GetoptError:
        print(usage)
        exit(1)

    for opt, arg in opts:
        if opt in ("-a", "--address"):
            server_ip = str(arg)
        else:
            print(f"unknown option: {opt}")
            print(usage)
            exit(1)

    game = Game(server_ip)
    game.run()
