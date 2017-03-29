from http.client import HTTPConnection
from jframework.modules.banner._banner import _Banner


class Httpservice(_Banner):

    def check(self):
        try:
            http = HTTPConnection(host=self.host, port=self.single_port, timeout=2)
            http.request("HEAD", "/")
            server = http.getresponse().getheader('server')
            return server
        except:
            print("Connection refused")
            return None


