import abc
import re
import socket
import jframework.extras.writeformat as wf
import sys


#Basic module
class Module(metaclass=abc.ABCMeta):

    def __init__(self):
        self.HOST = "127.0.0.1"
        self.abortar = False

    @abc.abstractmethod
    def run(self, session=[]):
        print("Work in progress")

    def help(self):
        print("--- Operations allowed ---")
        print("load module -> Load the module to use")
        print("help -> Show the help")
        print("ip <host> -> Set the IP target (Default: 127.0.0.1)")
        print("conf -> Show configuration")
        print("show_modules -> List all modules availables")
        print("show_sessions -> List the open sessions")
        print("session <id> -> Select session")
        print("delete_session <id> -> Remove session")
        print("exit -> Exit tool")

    def ip(self, dir):
        dir2 = ""
        try:
            dir2 = socket.gethostbyname(dir)
        except:
            pass
        ipregex = re.compile("^([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])$")
        if(ipregex.match(dir2) is None):
            print("✕ IP address is invalid")
        else:
            print("IP settings: " + str(dir2))
            self.HOST = dir2

    def conf(self):
        print("--- Configuration ---")
        wf.printf("OPTION", "VALUE", "DESCRIPTION", "REQUIRED")
        wf.printf("------", "-----", "-----------", "--------")
        wf.printf("ip", self.HOST, "IP target")

    def set_abortar(self):
        self.abortar = True


# Module whit ports configuration
class ModulePorts(Module):

    def __init__(self):
        super(ModulePorts, self).__init__()
        self.PORTS = [80]

    def help(self):
        super(ModulePorts, self).help()
        print("ports <1[,2,n]> -> Set the ports")

    def ports(self, p):
        print("Port/s setting: " + str(p))
        listaP = p.split(",")
        for i in range(0, len(listaP)):
            listaP[i] = listaP[i].strip(" ")
            try:
                if(int(listaP[i]) <= 0 or int(listaP[i]) > 65535):
                    raise Exception()
            except:
                print("✕ Error configuring ports")
                return
        self.PORTS = listaP

    def conf(self):
        super(ModulePorts, self).conf()
        wf.printf("ports", ','.join(map(str,self.PORTS)), "Ports configuration")