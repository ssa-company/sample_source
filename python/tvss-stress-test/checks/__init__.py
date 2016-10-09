
__author__ = "Sergey Soldatov"

import os
import glob
import sys
import inspect

sys.path.append(sys.path[0] + '../common')
sys.path.append(sys.path[0] + '../services')
sys.path.append(sys.path[0] + '../devices')
sys.path.append(sys.path[0] + '/checks')

modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in modules]

def __get_test():
    data = {}
    for name in __all__:
        if name != "__init__":
            mod = __import__(name)
            for n, obj in inspect.getmembers(mod):
                if inspect.isclass(obj) and inspect.getmodule(obj).__name__ == name:
                    test = {obj.test_name : getattr(inspect.getmodule(obj), obj.__name__)}
                    data.update(test) 
    return data

tests_list = __get_test()