import getpass
import pexpect
import sys
import signal


def signal_handler(signal, frame):
    print("")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_root(module):
    cont = input("This task needs root, do you want to convert root?(Y/N) ")
    if(cont.lower() != "y"):
        print("[!!] The module will be load, but you couldn't use it")
        return -1

    command = pexpect.spawn("sudo python3 jf.py")
    index = command.expect('password*', timeout=4)

    while index == 0:
        password = getpass.getpass("[*] Write your root password: ")
        command.sendline(password)
        try:
            index = command.expect(['password*',"jf >>*"], timeout=4)
            if index == 0:
                print("The password is incorrect, try again")
        except:
            index = -1

    if index == 1:
        print("Now you're root, to exit root mode write exit or press CTRL + C")
        command.write("load %s\n"%module)
        command.interact()  # Give control of the child to the user
    else:
        print("bad password, no root")
        command.kill(0)
    return 1