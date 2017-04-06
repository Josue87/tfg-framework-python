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

class Synscan(ModulePorts):

    def __new__(cls, *args, **kwargs):
        if os.getuid() != 0:
            # getRoot
            use = get_root("scan/synscan")
            if use >= 0:
                print("Now you don't have root permissions")
                return -1 # Can't load again

        return super(Synscan, cls).__new__(cls)

    def run(self):
        resp = check()
        if(resp != "ok"):
            print(resp)
            return

        existOpen = False
        for port in self.ports_list:
            port = int(port)
            port_src = RandShort()
            packet_ip = IP(dst=self.host)
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
