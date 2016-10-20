import sys
import os
import importlib


def loadModule(module):
    moduleAux = ""
    try:
        path = os.path.dirname(os.path.realpath('__file__'))
        path = os.path.join(path, "jframework/modules")
        new_module = module.split("/")
        path = os.path.join(path, '/'.join(new_module[:-1]))
        sys.path.append(path)
        moduleAux = importlib.import_module(new_module[-1])
        myClass = getattr(moduleAux, new_module[-1].capitalize())()
    except Exception as e:
        print(e)
        return None

    return myClass
