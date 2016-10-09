#!/usr/bin/python
# -*- coding: utf8 -*-

# Tests HASP.
# We stop/start HASP key service

import sys, inspect
import common.utils as utils
from common.utils import logger
from common.test.simple import simple
from common.test.complex import complex
from common.test.complex_thread import complex_thread

from services.hasp import hasp
from common.service.service import Service_State

#---------------------------------------------------------------
#----------------------- Simple tests --------------------------
#---------------------------------------------------------------

# Change hasp state
class hasp_test_restart(simple):
    test_name = "Hasp test restart"
    test_desc = "Тест для отключения/включения HASP ключа" 
    
    def __new__(cls):
        inst = simple.__new__(cls, target=hasp())
        return inst
        
    def __init__(self):
        simple.__init__(self, name=self.test_name)    
        
    def save_init_state(self):
        simple.save_init_state(self)
        n = {"state_hasp" : self.target.state}
        self.init_state.update(n) 
    
    def return_init_state(self):
        if self._runned == False: return
        simple.return_init_state(self)
        if self.init_state["state_hasp"] != self.target.state:
            if self.init_state["state_hasp"] == Service_State.run:   
                self.target.start()
            elif self.init_state["state_hasp"] == Service_State.stop:   
                self.target.stop()   
        
    def handler(self):
        simple.handler(self)
        if (utils.random_true()) and self.target.state == Service_State.stop: self.target.start()
        elif self.target.state == Service_State.start: self.target.stop()
        
#---------------------------------------------------------------
#---------------------- Complex tests --------------------------
#---------------------------------------------------------------

class hasp_complex(complex):      
    test_name = "Hasp complex test"
    test_desc = "Комплексный тест для HASP ключа"
    
    def __new__(cls):
        inst = complex.__new__(cls, target=hasp())
        return inst
    
    def __init__(self):
        complex.__init__(self, name=self.test_name)    
        self.append('hasp_test_restart', hasp_test_restart())
    
#---------------------------------------------------------------
#------------------- Complex thread tests ----------------------
#---------------------------------------------------------------

class hasp_complex_thread(complex_thread):
    test_name = "Hasp complex thread test"
    test_desc = "Комплексный циклический тест для HASP ключа"
    
    def __new__(cls, **parameters):
        inst = complex_thread.__new__(cls, target=hasp())
        return inst
    
    def __init__(self, **parameters):
        complex_thread.__init__(self, name=self.test_name, **parameters)    
        self.append('hasp_test_restart', hasp_test_restart())
    