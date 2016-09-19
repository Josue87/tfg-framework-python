import readline
import re
import os


class MyCompleter():

    def __init__(self, commands):
        self.COMMANDS = commands

    def _list_directories(self, root, route):
        my_list = []
        new_root = os.path.join(route,root)
        for name in os.listdir(new_root):
            if os.path.isdir(os.path.join(new_root, name)):
                name += os.sep
            if("model" not in name and name[0] != "_"):
                my_list.append(name.split(".py")[0])
        return my_list

    def _complete_path(self, path=None, route="jramework/modules"):
        if not path:
            return self._list_directories(".", route)
        directory = os.path.split(path)

        if directory[0]:
            dir_tmp = directory[0]
        else:
            dir_tmp = "."

        my_list = [os.path.join(directory[0], new_path)
               for new_path in self._list_directories(dir_tmp, route) if new_path.startswith(directory[1])]

        if len(my_list) > 1 or not os.path.exists(path):
            return my_list

        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._list_directories(path, route)]

        return [path + ' ']

    def complete_load(self, args):
        path = os.path.join("jframework", "modules")
        if not args:
            return self._complete_path(route=path)
        
        return self._complete_path(args[-1], path)
    
    def complete_file(self, args):
        path = os.path.join("jframework", "files")
        if not args:
            return self._complete_path(route=path)

        return self._complete_path(args[-1], path)

    def complete(self, text, state):
        buffer = readline.get_line_buffer()
        line = buffer.split()

        if not line:
            return [cmd + ' ' for cmd in self.COMMANDS][state]

        EXPR = re.compile('.*\s+$', re.M)

        if EXPR.match(buffer):
            line.append('')

        command = line[0].strip()

        if command in self.COMMANDS:
            command_function = getattr(self, 'complete_%s' % command)
            args = line[1:]
            if args:
                return (command_function(args) + [None])[state]
            return [command + ' '][state]
        results = [cmd + ' ' for cmd in self.COMMANDS if cmd.startswith(command)] + [None]

        return results[state]


