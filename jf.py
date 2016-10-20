from jframework.shell import Shell
from sys import exit
from os import _exit


if __name__ == "__main__":
    try:
        Shell().start()
    except KeyboardInterrupt:
        print(chr(27) + "[1;31m")
        print(" ⚠ Inrerrupted")
        print(chr(27) + "[0m")
        try:
            exit(0)
        except SystemExit:
            _exit(0)