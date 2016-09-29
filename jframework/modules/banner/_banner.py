from jframework.modules.model import Module
import jframework.extras.writeformat as wf
import os
import abc

class _Banner(Module, metaclass=abc.ABCMeta):

    def __init__(self):
        super(_Banner, self).__init__()
        self.FILE_READ = ""

    def help(self):
        options = super(_Banner, self).help()
        print("file <number_file> -> set de file with lines service:cve")

    def get_options(self):
        options = super(_Banner,self).get_options()
        options.extend(["file"])
        return options

    def file(self, f):
        self.FILE_READ = f

    def readFile(self):
        vulnerable = []
        cve = []
        try:
            if "/" not in self.FILE_READ:
                self.FILE_READ = os.path.join("jframework/files", self.FILE_READ)

            fileread = open(self.FILE_READ, "r")
            for line in fileread:
                l = line.split(" ")
                vulnerable.append(l[0])
                cve.append(l[1])
            fileread.close()
        except:
            print("It isn't possible read the file: " + str(self.FILE_READ))
            return None, None

        return vulnerable, cve

    def conf(self):
        super(_Banner, self).conf()
        thisfile = self.FILE_READ.split("/")
        if(thisfile is not None and thisfile[0].strip(" ") == ""):
            thisfile = "\' \'"
        else:
            thisfile = thisfile[-1]
        wf.printf("file", thisfile, "File whit vulnerabilities [service:cve]", "No")

    @abc.abstractmethod
    def check(self):
        pass

    def run(self):
        super(_Banner, self).run()
        banner = self.check()
        if(banner is None):
            return
        banner = banner.strip("\n")
        if(self.FILE_READ != ""):
            vulnerable, cve = self.readFile()
            if(vulnerable is None or cve is None):
                return
            isVulnerable = False
            try:
                index = 0
                for vuln in vulnerable:
                    if vuln.lower() in banner.lower():
                        print(str(self.HOST) + " is vulnerable: " + str(cve[index].strip()))
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



