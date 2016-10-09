#!/usr/bin/python
# -*- coding: utf8 -*-

from common.utils import logger

from test import test

class simple(test):
    
    def __new__(cls, **parameters):
        logger.debug("New simple test")
        inst = test.__new__(cls, **parameters)
        return inst
    
    def __init__(self, **parameters):
        logger.debug("Init simple test")
        test.__init__(self, **parameters)
    
    def handler(self):
        logger.debug("Run simple test %s", self.name)
        test.handler(self)
    
        