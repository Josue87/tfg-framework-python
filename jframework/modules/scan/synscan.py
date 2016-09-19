import socket
import logging
# Disable warning IPv6
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import os
from jframework.modules.model import ModulePorts
try:
    from scapy.all import *
    hasScapy = True
except:
    print("✕ It's required install scapy module to run syn scan")
    hasScapy = False


class Synscan(ModulePorts):

    def __init__(self):
        super(Synscan, self).__init__()
        conf.verb = 0  # scapy don't show info
        if (os.getuid() != 0):
            print("Attention: this task requires root")

    def run(self):
        super(Synscan, self).run()
        if(os.getuid() != 0):
            print("This task requires root")
            return
        if(not hasScapy):
            print("It's required install scapy module")
            return

        existOpen = False
        for port in self.PORTS:
            port = int(port)
            port_src = RandShort()
            packet_ip = IP(dst=self.HOST)
            packet = packet_ip / TCP(sport=port_src, dport=port, flags="S")
            answer = sr1(packet, timeout=2)
            if("NoneType" in str(type(answer))):
                pass
            elif(answer.haslayer(TCP) and answer.getlayer(TCP).flags == 0x12):
                existOpen = True
                p = packet_ip / TCP(sport=port_src, dport=port, flags="R")
                sr(p, timeout=1)
                try:
                    service = socket.getservbyport(port)
                except Exception as e:
                    print(e)
                    service = "¿?"
                print("[OPEN] " + str(port) + " -> " + str(service))

        if(not existOpen):
            print("In your list there aren't open ports")