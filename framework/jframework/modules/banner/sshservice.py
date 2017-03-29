import socket
from jframework.modules.banner._banner import _Banner


class Sshservice(_Banner):

    def __init__(self):
        super(Sshservice,self).__init__()
        self.single_port = 22

    def check(self):
        s = socket.socket()
        try:
            s.connect((self.host, self.single_port))
            data = s.recv(1024)
            return data.decode("utf-8")
        except:
            print("Connection refused")
            return None
