from jframework.modules.model import ModuleSinglePort
import jframework.extras.writeformat as wf
import os
import abc

class _Banner(ModuleSinglePort, metaclass=abc.ABCMeta):

    def __init__(self):
        super(_Banner, self).__init__()
        self.file_read = ""

    def get_options(self):
        options = super(_Banner,self).get_options()
        options.extend(["file"])
        return options

    def file(self, f):
        print("File: " + f)
        self.file_read = f

    def readFile(self):
        vulnerable = []
        cve = []
        try:
            if "/" not in self.file_read:
                self.file_read = os.path.join("jframework/files", self.file_read)

            fileread = open(self.file_read, "r")
            for line in fileread:
                l = line.split(" ")
                vulnerable.append(l[0])
                cve.append(l[1])
            fileread.close()
        except:
            print("It isn't possible read the file: " + str(self.file_read))
            return None, None

        return vulnerable, cve

    def conf(self):
        super(_Banner, self).conf()
        thisfile = self.file_read.split("/")
        if(thisfile is not None and thisfile[0].strip(" ") == ""):
            thisfile = "\' \'"
        else:
            thisfile = thisfile[-1]
        wf.printf("file", thisfile, "File whit vulnerabilities [service:cve]", "No")

    @abc.abstractmethod
    def check(self):
        pass

    def run(self):
        banner = self.check()
        if(banner is None):
            return
        banner = banner.strip("\n")
        if(self.file_read != ""):
            vulnerable, cve = self.readFile()
            if(vulnerable is None or cve is None):
                return
            isVulnerable = False
            try:
                index = 0
                for vuln in vulnerable:
                    if vuln.lower() in banner.lower():
                        print(str(self.host) + " is vulnerable: " + str(cve[index].strip()))
                        isVulnerable = True
                        break
                    else:
                        index += 1
            except:
                pass

            if(not isVulnerable):
                print("No vulnerabilities found")
        else:
            print("Service: "+str(banner))