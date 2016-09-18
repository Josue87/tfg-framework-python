import sys
import os
import importlib


def loadModule(module):
    moduleAux = ""
    try:
        path = os.path.dirname(os.path.realpath('__file__'))
        path = os.path.join(path, "jframework/modules")
        new_module = module.split("/")
        path = os.path.join(path, new_module[0])
        sys.path.append(path)
        moduleAux = importlib.import_module(new_module[1])
       # moduleAux = __import__(module)
        all_modules = dir(moduleAux)

        myClass = getattr(moduleAux, new_module[1].capitalize())()

    except Exception as e:
        print(e)
        print("error")
        return None

    return myClass
