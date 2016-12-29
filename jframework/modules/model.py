import abc
import re
import socket
import jframework.extras.writeformat as wf


#Basic module
class Module(metaclass=abc.ABCMeta):

    def __init__(self):
        self.host = "127.0.0.1"

    @abc.abstractmethod
    def run(self):
        pass

    def get_options(self):
        return ["ip"]

    def help(self):
        print("")
        print("______   MODULE   _______")
        print("back -> Remove loaded module")
        print("put <option> <parameter> -> Set the options")
        print("conf -> Show configuration")

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
            self.host = dir2

    def conf(self):
        print("--- Configuration ---")
        wf.printf("OPTION", "VALUE", "DESCRIPTION", "REQUIRED")
        wf.printf("------", "-----", "-----------", "--------")
        wf.printf("ip", self.host, "IP target")

class ModuleSinglePort(Module, metaclass=abc.ABCMeta):
    def __init__(self):
        super(ModuleSinglePort, self).__init__()
        self.single_port = 80  # Las que requieran puerto 80 por defecto, no necesitarán llamar a __init__

    def get_options(self):
        options = super(ModuleSinglePort, self).get_options()
        options.append("port")
        return options

    def port(self, p):
        print("Port setting: " + p)
        try:
            if (int(p) <= 0 or int(p) > 65535):
                raise Exception()
            else:
                self.single_port = p
        except:
            print("✕ Error configuring port")

    def conf(self):
        super(ModuleSinglePort, self).conf()
        wf.printf("port", str(self.single_port), "Port configuration")


# Module whit ports configuration
class ModulePorts(Module, metaclass=abc.ABCMeta):

    def __init__(self):
        super(ModulePorts, self).__init__()
        self.ports_list = [80]

    def get_options(self):
        options = super(ModulePorts,self).get_options()
        options.append("ports")
        return options

    def ports(self, p):
        print("Port/s setting: " + p)
        listaP = p.split(",")
        for i in range(0, len(listaP)):
            try:
                if listaP[i] != "":
                    listaP[i] = int(listaP[i].strip())
                    if(int(listaP[i]) <= 0 or int(listaP[i]) > 65535):
                        raise Exception()
                else:
                    del listaP[i]
            except:
                print("✕ Error configuring ports")
                return
        self.ports_list = listaP

    def conf(self):
        super(ModulePorts, self).conf()
        ports = ""
        i = 0
        for p in self.ports_list:
            ports += str(p)
            i += 1
            if(len(self.ports_list) <= i):
                break
            ports += ","

            if i>= 5:
                ports += "..."
                break

        wf.printf("ports", ports, "Ports configuration")