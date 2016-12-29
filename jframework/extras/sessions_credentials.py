from jframework.extras.console import terminal

class Check:
    @staticmethod
    def exist_in_list(origin_list, element):
        for el in origin_list:
            if el["user"] == element["user"] and el["type"] == element["type"] and el["ip"] == element["ip"]:
                try:
                    if(element["session"]):
                        element["session"].close()
                except:
                    pass
                return True
        return False

class Session:

    def __init__(self):
        self.sessions = []

    def list_sessions(self):
        if (len(self.sessions)):
            print(chr(27) + "[1;34m")
            print("{:5}\t{:16}\t\t{:9}\t\t{:8}".format("ID", "HOST", "User", "Type"))
            print(chr(27) + "[0m")
            for s in self.sessions:
                print("{:5}\t{:16}\t\t{:9}\t\t{:8}".format(s["id"], s["ip"], s["user"], s["type"]))
            print("")
        else:
            print("There are no sessions")

    def start_session(self, id):
        my_session = None

        for s in self.sessions:

            if (str(s["id"]) == str(id)):
                my_session = s
                break

        if (my_session is not None):
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
            if (str(s["id"]) == str(id)):
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

    def return_result_session(self, res):
        if res is None or len(res) == 0:
            return

        for session in res:
            if(Check.exist_in_list(self.sessions, session)):
                continue
            session["id"] = self.get_id_session()
            self.sessions.append(session)

    def get_id_session(self):
        id = 1
        for s in self.sessions:
            if(s["id"] >= id):
                id = s["id"] + 1
        return id

    def close_sessions(self):
        if(len(self.sessions) == 0):
            return
        for s in self.sessions:
            try:
                s["session"].close()
            except:
                pass

class Credential:

    def __init__(self):
        self.credentials = []

    def list_credentials(self):
        if(len(self.credentials)):
            print(chr(27) + "[1;34m")
            print("{:16}\t{:20}\t\t{:8}".format("HOST", "User:Password", "Type"))
            print(chr(27) + "[0m")
            for c in self.credentials:
                print("{:16}\t{:20}\t\t{:8}".format(c["ip"], c["user"] + ":" + c["password"], c['type'] ))
            print("")
        else:
            print("There are not credentials yet")

    def return_result_credential(self, res):
        if res is None or len(res) == 0:
            return

        for credential in res:
            if (Check.exist_in_list(self.credentials, credential)):
                continue
            self.credentials.append(credential)