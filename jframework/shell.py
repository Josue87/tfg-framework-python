import os
import sys
import signal
from jframework.extras.load import loadModule
from jframework.extras.exceptions import MyError
from jframework.extras.autocomplete import MyCompleter
from jframework.extras.console import terminal
import atexit
import readline
import concurrent.futures


class Shell():

    def __init__(self):
        self.myModule = None
        self.nameModule = None
        self.sessions = []
        self.future_result = None

    def prompt(self, module=None):
        if (module is None):
            return "⚤ >> "
        else:
            return "⚤ (\001\033[91m\002" + str(module) + "\001\033[0m\002) >> "

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
            i = 0
            for s in self.sessions:
                print(s["id"], "\t", s["ip"] ,"\t", s["user"],"\t[" + s["type"] + "]")
                i += 1
        else:
            print("There are no sessions")

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
                self.delete_session(my_session[id])
        else:
            print("Session", id, "not found")

    def delete_session(self, id):
        my_session = None
        i = 0
        for s in self.sessions:
            if (str(s["id"]) == id):
                my_session = s
                break
            i += 1
        if (my_session is not None):
            self.sessions.remove(my_session)
            my_session["session"].close()
            print("Close session", id)
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

    def start(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        completer = MyCompleter(["exit", "load", "show_modules",
                       "help", "conf", "ports", "ip", "users", "verbose",
                       "passwords", "run", "file", "show_sessions", "session", "delete_session"])

        readline.set_history_length(40)  #max 40
        readline.set_completer_delims(' \t\n;')  # override the delims (I want /)
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completer.complete)

        operation = ""
        self.draw_init()
        while operation.lower() != "exit":
            if(self.myModule is None):
                operation = input(self.prompt())
            else:
                operation = input(self.prompt(self.nameModule.split("/")[1]))

            operation = operation.strip()
            op = self.strip_own(operation)

            if(not op):
                continue

            op[0] = op[0].lower()

            if(op[0] == "exit"):
                break

            if(op[0] != '' and op[0] != "exit"):
                if(op[0] == "show_modules"):
                    self.listModules()
                    continue

                if(op[0] == "show_sessions"):
                    self.list_sessions()
                    continue

                if(op[0] != 'load' and op[0] != "session" and
                           op[0] != "delete_session" and self.myModule is None):
                    print("⚠ First load a module")
                    print("The syntax is load module")
                    print("To show the modules availables: show_modules")
                    continue

                try:
                    if(len(op) == 1):
                        if(op[0] == "run"):
                            executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
                            self.future_result = executor.submit(self.myModule.run)
                            self.future_result.add_done_callback(self.return_result)
                            while(not self.future_result.done()):
                                pass
                        else:
                            getattr(self.myModule, op[0])()
                    else:
                        if(op[0] == "load"):
                            self.myModule = self.load_module(op[1].strip().lower())
                            self.nameModule = op[1].strip()
                        elif(op[0] == "session"):
                            self.start_session(op[1])
                        elif(op[0] == "delete_session"):
                            self.delete_session(op[1])
                        else:
                            getattr(self.myModule, op[0])(op[1])
                except MyError as e:
                    print(e)
                except Exception as e:
                    print("⚠ The operation" + str(op[0]) +
                    " isn't permit, use help command.")
                    print(e)
        self.close_sessions()
        print("[*] The tool has been closed.")

    def strip_own(self, line):
        mylist = line.split(" ")
        while "" in mylist:
            mylist.remove("")
        return mylist

    def close_sessions(self):
        i = 0
        for s in self.sessions:
            try:
                s["session"].close()
            except:
                pass

    def return_result(self, future):
        if future.result() is None:
            return
        for session in future.result():
            session["id"] = self.get_id_session()
            self.sessions.append(session)

    def get_id_session(self):
        id = 1
        for s in self.sessions:
            if(s["id"] >= id):
                id = s["id"] + 1
        return id

    def signal_handler(self, signal, frame):
            if(self.future_result is not None and self.future_result.running()):
                print("Abort!")
                self.myModule.set_abortar()
            else:
                print('\nThe tool has been closed: Ctrl + C')
                self.close_sessions()
                sys.exit(0)

