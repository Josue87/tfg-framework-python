def terminal(client, prompt, type):
    if(type == "ssh"):
        terminal_ssh(client, prompt)
    else:
        print("No terminal")

def terminal_ssh(client, prompt):
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