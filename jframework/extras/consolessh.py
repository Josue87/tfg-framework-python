def terminal_ssh(client, prompt):
    command = ""
    while command.lower().strip(" ") != "exit":
        command = input("\001\033[96m\002" + prompt + "> \001\033[0m\002")
        try:
            stdin, stdout, stderr = client.exec_command(command)
            data = stderr.readlines()

            if (not data):
                data = stdout.readlines()

            for line in data:
                print(line, end="")
        except:
            print("✕ Session error")