from ftplib import FTP
from jframework.modules.banner._banner import _Banner


class Ftpservice(_Banner):

    def __init__(self):
        super(Ftpservice,self).__init__()
        self.single_port = 21

    def check(self):
        ftp = FTP()
        try:
            # ftp abierto '193.43.36.131'
            ftp.connect(host=self.host, port=self.single_port, timeout=7)
            return ftp.getwelcome()
        except:
            print("Connection refused")
            return None
