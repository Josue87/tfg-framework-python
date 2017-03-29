from jframework.extras.autocomplete import MyCompleter
import readline



def terminal(client, prompt, type):
    if(type == "ssh"):
        terminal_ssh(client, prompt)
    elif(type == "ftp"):
        terminal_ftp(client, prompt)
    else:
        print("No terminal")

def terminal_ssh(client, prompt):
    completer = MyCompleter(["scp", "whoami", "cd", "ls", "exit" ], None)
    readline.set_completer(completer.complete)
    print("You are in a ssh session")
    command = ""
    while command.lower().strip(" ") != "exit":
        command = input("\001\033[96m\002" + prompt + "> \001\033[0m\002")
        stdin, stdout, stderr = client.exec_command(command)
        data = stderr.readlines()
        if (not data):
            data = stdout.readlines()

        for line in data:
            print(line, end="")

def terminal_ftp(client, prompt):
    completer = MyCompleter(["cwd", "dir","pwd", "exit"], None)
    readline.set_completer(completer.complete)
    print("You are in a ftp session")
    command = ""
    while command.lower().strip(" ") != "exit":
        command = input("\001\033[96m\002" + prompt + "(ftp)> \001\033[0m\002")
        if("exit" in command.lower()):
            return
        try:
            c = command.strip(" ").split(" ")
            if(c[1:]):
                parameter = ""
                for par in c[1:]:
                    parameter.join(" "+par)
                line = getattr(client, c[0])(parameter)
            else:
                line = getattr(client, c[0])()
            print(line)
        except Exception as e:
            print("Error in", command)
            print(e)
