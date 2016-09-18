from jframework.modules.model import Module
from jframework.extras.consolessh import terminal_ssh
hasParamiko = True
try:
    import paramiko
except:
    print("✕ It's required install paramiko module to run openssh")
    hasParamiko = False


class Sshlogin(Module):
    def run(self, session):
        if(not hasParamiko):
            print("It's required install paramiko module")
            return
        print("Inser user and password to connect with ssh")
        print("If you want to exit, don't write user")
        while True:
            user = input("User: ")
            if(user == ""):
                break
            password = input("Password: ")
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(self.HOST, username=user, password=password)
                print("SUCCESS: " + str(user) + ":" + str(password))
                print("Write exit to go out")
                terminal_ssh(client, str(self.HOST) + ".ssh")
                break
            except Exception as e:
                if("Authentication failed." == str(e)):
                    print(e)
                else:
                    print("Service ssh not found")
                    break

            client.close()
