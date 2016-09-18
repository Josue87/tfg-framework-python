from ftplib import FTP
from jframework.modules.banner._banner import _Banner


class Ftpservice(_Banner):

    def check(self):
        ftp = FTP()
        try:
            # ftp abierto '193.43.36.131'
            ftp.connect(self.HOST, self.PORTS[0])
            return ftp.getwelcome()
        except:
            print("Connection refused")
            return None
