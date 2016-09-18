import socket
from jframework.modules.banner._banner import _Banner


class Sshservice(_Banner):

    def check(self):
        s = socket.socket()
        try:
            s.connect((self.HOST, 22))
            data = s.recv(1024)
            return data.decode("utf-8")
        except:
            print("Connection refused")
            return None
