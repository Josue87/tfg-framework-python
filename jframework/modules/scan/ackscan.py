import logging
# Disable warning IPv6
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import os
from jframework.modules.model import ModulePorts
try:
    from scapy.all import *
    hasScapy = True
except:
    print("✕ It's required install scapy module to run ack scan")
    hasScapy = False


class Ackscan(ModulePorts):

    conf.verb = 0  # scapy don't show info

    def run(self, sessions):
        super(Ackscan, self).run()
        if(os.getuid() != 0):
            print("This task requires root")
            return
        if(not hasScapy):
            print("It's required install scapy module")
            return

        for port in self.PORTS:
            port = int(port)
            port_src = RandShort()
            packet_ip = IP(dst=self.HOST)
            packet = packet_ip / TCP(sport=port_src, dport=port, flags="A")
            response = sr1(packet, timeout=2)
            if("NoneType" in str(type(response))):
                print("[!] " + str(port) + " has firewall")
            elif(response.haslayer(TCP) and response.getlayer(TCP).flags == 0x4):
                print("[OK] " + str(port) + " hasn't firwall")
            elif(response.haslayer(ICMP) and int(response.getlayer(ICMP).type) == 3):
                if(response.getlayer(ICMP).code in [1, 2, 3, 9, 10, 13]):
                    print("[!] " + str(port) + " has firewall")