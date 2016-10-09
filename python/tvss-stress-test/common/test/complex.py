#!/usr/bin/python
# -*- coding: utf8 -*-

from common.utils import logger

from test import test

class complex(test):
    __list = {}
    
    @property
    def list(self):
        return self.__list
    
    def __new__(cls, **parameters):
        logger.debug("New complex test")
        inst = test.__new__(cls, **parameters)
        return inst
    
    def __init__(self, **parameters):
        logger.debug("Init complex test")
        self.__list = {}
        test.__init__(self, **parameters)

    # Добавить тест в список
    def append(self, name, test):
        if test is not None: self.__list[name ] = test  
        
    def handler(self):
        logger.debug("Complex test %s", self.name)
        for val in self.__list.values(): val.run()
    