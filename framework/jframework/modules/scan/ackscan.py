import logging
# Disable warning IPv6
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from jframework.modules.model import ModulePorts
from jframework.extras.check_scapy import check
from jframework.extras.root import get_root
try:
    from scapy.all import *
    conf.verb = 0
except:
    pass


class Ackscan(ModulePorts):

    def __new__(cls, *args, **kwargs):
        if os.getuid() != 0:
            # getRoot
            use = get_root("scan/ackscan")
            if use >= 0:
                print("Now you don't have root permissions")
                return -1 # Can't load again

        return super(Ackscan, cls).__new__(cls)

    def run(self):
        resp = check()
        if (resp != "ok"):
            print(resp)
            return

        for port in self.ports_list:
            port = int(port)
            port_src = RandShort()
            packet_ip = IP(dst=self.host)
            packet = packet_ip / TCP(sport=port_src, dport=port, flags="A")
            response = sr1(packet, timeout=2)
            if("NoneType" in str(type(response))):
                print("[!] " + str(port) + " has firewall")
            elif(response.haslayer(TCP) and response.getlayer(TCP).flags == 0x4):
                print("[OK] " + str(port) + " hasn't firwall")
            elif(response.haslayer(ICMP) and int(response.getlayer(ICMP).type) == 3):
                if(response.getlayer(ICMP).code in [1, 2, 3, 9, 10, 13]):
                    print("[!] " + str(port) + " has firewall")