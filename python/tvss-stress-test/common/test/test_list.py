#!/usr/bin/python
# -*- coding: utf8 -*-

# Common class for test

import sys
from collections import OrderedDict

from common.utils import logger
from checks import tests_list as tests

class test_list(object):
    __name = None           # Название списка
    __data = {}             # Перечень тестов
    __id = 0
    
    @property
    def name(self):
        return self.__name
    
    def __init__(self, name):
        self.__name = name
        logger.debug("Init test list %s", name)
    
    # Добавить тест в список
    def append(self, test_name, **parameters):
        logger.info("Append name \"%s\" " % (test_name))
        if parameters=={}:
            obj = tests[test_name]()
        else:
            obj = tests[test_name](**parameters)
            
        if obj is not None: 
            logger.debug("Appended name \"%s\" " % (test_name))
            self.__data[test_name + str(self.__id)] = obj  
            self.__id = self.__id + 1

    # Запустить проход по тестам
    def run(self):
        test_size = len(self.__data.keys())
        i = 0.0
        for val in self.__data.values():
            sys.stdout.write("\rTesting progress %d%% \n" % i)
            sys.stdout.flush()
            i = i + 100 / test_size
            val.run()
        sys.stdout.write("\rTesting progress 100% \n")
        sys.stdout.flush()    
            
    def return_init_state(self):  
        for val in self.__data.values():
            val.return_init_state()        
            