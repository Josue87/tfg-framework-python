import os
import readline
import atexit

if (os.getuid() != 0):
    historyPath = os.path.expanduser("~/.jfhistory")
else:
    historyPath = os.path.expanduser("~/.jfhistory_root")


def save_history(historyPath=historyPath):
    readline.write_history_file(historyPath)


def start_record():
    if os.path.exists(historyPath):
        readline.read_history_file(historyPath)

    atexit.register(save_history)