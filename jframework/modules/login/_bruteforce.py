from jframework.modules.model import Module
import jframework.extras.writeformat as wf
import abc
import threading

import queue


class _Bruteforce(Module, metaclass=abc.ABCMeta):

    def __init__(self):
        super(_Bruteforce,self).__init__()
        self.userFile = "jframework/files/users.txt"
        self.passwordFile = "jframework/files/passwords.txt"
        self.verb = True
        self.num_threads = 0
        self.login_found = 0
        self.maxthreads = 4

    def get_options(self):
        options = super(_Bruteforce,self).get_options()
        options.extend(["users", "passwords", "verbose", "threads"])
        return options

    @abc.abstractmethod
    def worker(self, user, password):
        pass

    def read_files(self):
        users_file = open(self.userFile, "r")
        passwords_file = open(self.passwordFile, "r")
        users = users_file.read().split("\n")
        passwords = passwords_file.read().split("\n")
        try:
            users_file.close()
            passwords_file.close()
        except:
            pass

        return users, passwords

    def run(self):
        super(_Bruteforce, self).run()
        try:
          users, passwords = self.read_files()
        except:
            print("✕ Error in some file")
            return

        self.login_found = 0
        print("This module can be slow. Patience.")
        threads = []

        for u in users:
            u2 = u.strip()
            for p in passwords:
                p = p.strip()
                while self.num_threads >= self.maxthreads:
                    pass

                th = threading.Thread(target=self.worker, args=(u2, p))
                threads.append(th)
                self.num_threads += 1
                th.start()

        for t in threads:
            t.join()

        print("Found", self.login_found, "logins")

    def users(self, u):
        self.userFile = u

    def passwords(self, p):
        self.passwordFile = p

    def threads(self,number):
        try:
            number = int(number)
        except:
            pass
        if(number > 10):
            self.maxthreads = 10
        elif(number < 0):
            self.maxthreads = 1
        else:
            self.maxthreads = number

    def verbose(self, v):
        if(v.lower() == "yes"):
            self.verb = True
        else:
            self.verb = False

    def help(self):
        super(_Bruteforce, self).help()
        print("threads <number> -> set the number of threads (1..10)")
        print("users <file_users> -> set the file with the users")
        print("passwords <file_passwords> -> set the file with the passwords")
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
        wf.printf("threads", str(self.maxthreads), "Number of threads(1..20)", "No")
        if(self.verb):
            v = "True"
        else:
            v = "False"
        wf.printf("verbose", v, "Show info", "No")

    def print_result(self,user, password, error=True):
        if error:
            print(chr(27) + "[1;31m[-] " + chr(27) + "[0m" + str(user) + ":" + str(password) + " >> failed")
        else:
            print(chr(27) + "[1;34m[+] " + chr(27) + "[0m" + str(user) + ":" + str(password) + " >> OK")
