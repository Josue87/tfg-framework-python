from jframework.modules.model import Module
import jframework.extras.writeformat as wf
import abc
import threading

MAXTHREADS = 4


class _Bruteforce(Module, metaclass=abc.ABCMeta):

    def __init__(self):
        super(_Bruteforce,self).__init__()
        self.userFile = "jframework/files/users.txt"
        self.passwordFile = "jframework/files/passwords.txt"
        self.verb = True
        self.num_threads = 0

    def get_options(self):
        options = super(_Bruteforce,self).get_options()
        options.extend(["users", "passwords", "verbose"])
        return options

    @abc.abstractmethod
    def worker(self, user, password):
        pass

    def run(self):
        super(_Bruteforce, self).run()
        try:
            users = open(self.userFile, "r")
            passwords = open(self.passwordFile, "r").read().split("\n")
        except:
            print("✕ Error in some file")
            return

        threads = []
        print("This module can be slow. Patience.")
        for u in users:
            u2 = u.strip()
            for p in passwords:
                p = p.strip()
                while self.num_threads >= MAXTHREADS:
                    pass

                th = threading.Thread(target=self.worker, args=(u2, p))
                threads.append(th)
                self.num_threads += 1
                th.start()

        for t in threads:
            t.join()

    def users(self, u):
        self.userFile = u

    def passwords(self, p):
        self.passwordFile = p

    def verbose(self, v):
        if(v.lower() == "yes"):
            self.verb = True
        else:
            self.verb = False

    def help(self):
        super(_Bruteforce, self).help()
        print("verbose <YES/NO> -> show info when a module is running")

    def conf(self):
        super(_Bruteforce, self).conf()
        try:
            uf = self.userFile.split("/")
            uf = uf[-1]
            pf = self.passwordFile.split("/")
            pf = pf[-1]
        except Exception as e:
            print(e)
        wf.printf("users", uf, "File whit the users")
        wf.printf("passwords", pf, "File whit passwords")
        if(self.verb):
            v = "True"
        else:
            v = "False"
        wf.printf("verbose", v, "Show info", "No")
