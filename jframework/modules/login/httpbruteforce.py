from jframework.modules.login._bruteforce import _Bruteforce
import jframework.extras.writeformat as wf
import urllib.request as ur
import http.client
import sys


class Httpbruteforce(_Bruteforce):

    def __init__(self):
        super(Httpbruteforce, self).__init__()
        self.realm_router = None
        self.resource_http = "/"

    def conf(self):
        super(Httpbruteforce, self).conf()
        wf.printf("resource", self.resource_http, "Resource that needs password", "No")

    def help(self):
        super(_Bruteforce, self).help()
        print("resource <name> -> set resource that needs password")

    def get_realm(self):
        try:
            conn = http.client.HTTPConnection(host=self.host, port=self.single_port, timeout=3)
            conn.request("GET", self.resource_http)
            res = conn.getresponse()
            realm = res.getheader("WWW-Authenticate").split("=")[1].strip("\"")
            return realm
        except Exception as e:
            if("refused" in str(e)):
                return "refused"
            return None

    def resource(self, res):
        if res[0] != "/":
            res = "/" + res
        self.resource_http = res

    def get_options(self):
        options = super(Httpbruteforce, self).get_options()
        options.extend(["resource"])
        return options

    def worker(self, user, password):

        try:
            auth_handler = ur.HTTPBasicAuthHandler()
            auth_handler.add_password(realm=self.realm_router,
                                      uri=self.host,
                                      user=user,
                                      passwd=password)
            opener = ur.build_opener(auth_handler)
            ur.install_opener(opener)
            pag = ur.urlopen("http://" + str(self.host) + self.resource_http)
            if (pag.getcode() == 200):
                self.print_result(user, password, error=False)
                self.lock.acquire()
                self.add_credential(user, password, "http")
                self.lock.release()
        except Exception as e:
            if("refused" in str(e)):
                self.num_threads -= 1
                self.error += 1
                sys.exit(0)
            if (self.verb):
                self.print_result(user, password, error=True)

        self.num_threads -= 1
        sys.exit(0)

    def run(self):
        self.realm_router = self.get_realm()

        if self.realm_router is None:
            print("No realm found")
            return

        if(self.realm_router == "refused"):
            print("Connection refused")
            return

        super(Httpbruteforce, self).run()

        return self.sessions, self.credentials