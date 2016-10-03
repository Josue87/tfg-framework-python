import os
from jframework.extras.load import loadModule
from jframework.extras.exceptions import MyError
from jframework.extras.autocomplete import MyCompleter
from jframework.extras.console import terminal
import atexit
import readline


class Shell():

    def __init__(self):
        self.myModule = None
        self.nameModule = None
        self.sessions = []
        self.credentials = []

    def prompt(self, module=None):
        if (module is None):
            return "jf >> "
        else:
            return "jf (\001\033[91m\002" + str(module) + "\001\033[0m\002) >> "

    if(os.getuid() != 0):
        historyPath = os.path.expanduser("~/.jfhistory")
    else:
        historyPath = os.path.expanduser("~/.jfhistory_root")

    def save_history(historyPath=historyPath):
        readline.write_history_file(historyPath)

    if os.path.exists(historyPath):
        readline.read_history_file(historyPath)

    atexit.register(save_history)

    def load_module(self, module):
        module_load = loadModule(module)
        if(module_load is None):
            raise MyError("✕ Error loading module %s" % module)
        print(str(module) + " loaded correctly")
        return module_load

    def listModules(self):
        for root, dirs, files in os.walk('jframework/modules'):
            for file in files:
                if ".py" == file[-3:] and file != "model.py" and file[0] != "_":
                    path = root.split("/")[-1]
                    print(path + "/" + file)

    def list_sessions(self):
        if(len(self.sessions)):
            print(chr(27) + "[1;34m")
            print("{:5}\t{:16}\t\t{:9}\t\t{:8}".format("ID","HOST","User", "Type"))
            print(chr(27) + "[0m")
            for s in self.sessions:
                print("{:5}\t{:16}\t\t{:9}\t\t{:8}".format(str(s["id"]), s["ip"] , s["user"], s['type']))
            print("")
        else:
            print("There are no sessions")

    def list_credentials(self):
        if(len(self.credentials)):
            print(chr(27) + "[1;34m")
            print("{:16}\t{:20}\t\t{:8}".format("HOST","User:Password", "Type"))
            print(chr(27) + "[0m")
            for c in self.credentials:
                print("{:16}\t{:20}\t\t{:8}".format(c["ip"], c["user"]+":"+c["password"], c['type'] ))
            print("")
        else:
            print("There are not credentials yet")

    def start_session(self, id):
        my_session = None
        i = 0
        for s in self.sessions:
            if(str(s["id"]) == id):
                my_session = s
                break
            i += 1
        if(my_session is not None):
            try:
                terminal(my_session["session"], my_session["ip"], my_session["type"])
            except:
                print("✕ Session error... Deleted")
                self.delete_session(id)
        else:
            print("Session", id, "not found")

    def delete_session(self, id):
        my_session = None
        for s in self.sessions:
            if (str(s["id"]) == id):
                my_session = s
                break
        if (my_session is not None):
            self.sessions.remove(my_session)
            try:
                my_session["session"].close()
            except:
                pass
            print("the session {} was closed".format(id))
        else:
            print("Session", id, "not found")

    def draw_init(self):
         print("""
         %%%%                %%%%
         %%%%%              %%%%%
         %%%%%%%          %%%%%%%
        %%%%%%%%%%%    %%%%%%%%%%%
         %%    %%%%%%%%%%%%    %%
                  %%%%%%
                %%%%%%%%%
               %%%%   %%%%%
           %%%%%%%      %%%%%%%
         %%%%%%%          %%%%%%%
        %%%%%%%            %%%%%%%
         %%%%%%            %%%%
            %%              %%

        """)

    def initial(self):
        self.completer = MyCompleter(["exit", "load", "modules", "show_sessions",
                                      "session", "delete_session", "credentials"], self)

        readline.set_history_length(40)  # max 40
        readline.set_completer_delims(' \t\n;')  # override the delims (I want /)
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.completer.complete)

    def get_module(self):
        return self.myModule

    def start(self):
        self.initial()
        operation = ""
        self.draw_init()
        while operation != "exit":
            if (self.myModule is None):
                operation = input(self.prompt())
            else:
                operation = input(self.prompt(self.nameModule.split("/")[1]))
            operation = operation.lower().strip()
            self.exec_command(operation)
        self.close_sessions()
        print("[*] The tool has been closed.")

    def first_exec(self,op):
        result = True
        if (len(op) == 0 or op[0] == "exit"):
            result = False
        elif (op[0] == "modules"):
            self.listModules()
            result = False
        elif (op[0] == "show_sessions"):
            self.list_sessions()
            result = False
        elif (op[0] == "credentials"):
            self.list_credentials()
            result = False

        return result

    def exec_command(self, operation):
        op = self.strip_own(operation)

        if (self.first_exec(op) and op[0] != ''):

            if (op[0] != 'load' and op[0] != "session" and
                        op[0] != "delete_session" and self.myModule is None):
                print("⚠ First load a module")
                print("The syntax is load module")
                print("To show the modules availables write: modules")
                return
            try:
                if (len(op) == 1):
                    if (op[0] == "run"):
                        try:
                            res_s, res_c = self.myModule.run()
                            self.return_result_session(res_s)
                            self.return_result_credential(res_c)
                        except:
                            pass
                    else:
                        getattr(self.myModule, op[0])()
                else:
                    if (op[0] == "load"):
                        self.myModule = self.load_module(op[1].strip())
                        self.nameModule = op[1].strip()
                        self.completer.extend_completer(["put", "run", "conf", "help"])
                    elif (op[0] == "session"):
                        self.start_session(op[1])
                        readline.set_completer(self.completer.complete)
                    elif (op[0] == "delete_session"):
                        self.delete_session(op[1])
                    else:
                        if (op[0] == "put"):
                            if (len(op) >= 3):
                                getattr(self.myModule, op[1])(op[2])
                            else:
                                print("Parameter is not found")
                                return
                        else:
                            getattr(self.myModule, op[0])(op[1])
            except MyError as e:
                print(e)
            except Exception as e:
                print("⚠ Error with operation " + str(op[0]) +
                      ". use help command.")
                print(e)

    def strip_own(self, line):
        mylist = line.split(" ")
        while "" in mylist:
            mylist.remove("")
        return mylist

    def close_sessions(self):
        if(len(self.sessions) == 0):
            return
        i = 0
        for s in self.sessions:
            try:
                s["session"].close()
            except:
                pass

    def return_result_session(self, res):
        if res is None or len(res) == 0:
            return

        for session in res:
            if(self.exist_in_list(self.sessions, session)):
                continue
            session["id"] = self.get_id_session()
            self.sessions.append(session)

    def return_result_credential(self, res):
        if res is None or len(res) == 0:
            return

        for credential in res:
            if (self.exist_in_list(self.credentials, credential)):
                continue
            self.credentials.append(credential)

    def exist_in_list(self,origin_list, element):
        for el in origin_list:
            if el["user"] == element["user"] and el["type"] == element["type"] and el["ip"] == element["ip"]:
                try:
                    if(element["session"]):
                        element["session"].close()
                except:
                    pass
                return True
        return False



    def get_id_session(self):
        id = 1
        for s in self.sessions:
            if(s["id"] >= id):
                id = s["id"] + 1
        return id