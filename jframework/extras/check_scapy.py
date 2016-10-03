import os

def check():
    try:
        from scapy.all import TCP
    except:
        return "It's required install scapy module"

    if(os.getuid() != 0):
        return "This task requires root"

    return "ok"
