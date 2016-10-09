#!/usr/bin/python
# -*- coding: utf8 -*-

import threading

import common.utils as utils
from common.utils import logger
from complex import complex

class complex_thread(complex):
    __thr = None
    __min = 0
    __max = 0
    
    def __new__(cls, **parameters):
        logger.debug("New complex thread test")
        inst = complex.__new__(cls, **parameters)
        return inst
    
    def __init__(self, **parameters):
        complex.__init__(self, **parameters)
        self.__thr = threading.Thread(target=self.thread, args=())
        self.__thr.daemon = True
        if parameters.get('min_sleep') is not None: self.__min = parameters['min_sleep']
        else: self.__min = 0
        if parameters.get('max_sleep') is not None: self.__max = parameters['max_sleep']
        else: self.__max = 30
        if self.__max <= self.__min:
            logger.warning("Bad random limits! Change to default (0;30)")
            self.__min = 0
            self.__max = 30
    
    def thread(self):
        while True:
            complex.run(self)
            utils.random_sleep(self.__min, self.__max)
            
    def run(self):
        self.__thr.start()
        
        

