#!/usr/bin/python
# -*- coding: utf8 -*-

# Test MOXA switch

import sys, inspect
import common.utils as utils
from common.utils import logger
from common.test.simple import simple
from common.test.complex import complex
from common.test.complex_thread import complex_thread

from devices.sw_moxa import sw_moxa

#---------------------------------------------------------------
#----------------------- Simple tests --------------------------
#---------------------------------------------------------------

class moxa_sw_test_restart_ports(simple):
    test_name = "SW MOXA test restart"
    test_desc = ""
    
    def __new__(cls, **parameters):
        if parameters.get('target') is not None:
                inst = simple.__new__(cls, target=parameters['target'])
        else: inst = simple.__new__(cls, target=sw_moxa(**parameters))
        return inst
        
    def __init__(self, **parameters):
        simple.__init__(self, name=self.test_name + " " + self.target.ip)    
        
    def save_init_state(self):
        simple.save_init_state(self)
        for item in self.target.ports:
            n = {item : self.target.check_iif_state(item)} 
            self.init_state.update(n) 
    
    def return_init_state(self):
        if self._runned == False: return
        simple.return_init_state(self) 
        for item in self.target.ports:
            if self.init_state[item] != self.target.check_iif_state(item):
                if self.init_state[item]: self.target.up_iff(item)
                else: self.target.down_iff(item)
                
    def port_test(self, id_iff):
        if (utils.random_true()): self.target.up_iff(id_iff)
        else: self.target.down_iff(id_iff)             
        
    def handler(self):
        simple.handler(self)
        for item in self.target.ports:
            self.port_test(item)

#---------------------------------------------------------------
#---------------------- Complex tests --------------------------
#---------------------------------------------------------------

class moxa_sw_complex(complex):
    test_name = "SW MOXA complex test"
    test_desc = ""
    
    def __new__(cls, **parameters):
        if parameters.get('target') is not None:
            inst = complex.__new__(cls, target=parameters['target'])
        else: inst = complex.__new__(cls, target=sw_moxa(**parameters))
        return inst

    def __init__(self, **parameters):
        complex.__init__(self, name=self.test_name + " " + self.target.ip)    
        self.append('moxa_sw_test_restart_ports', moxa_sw_test_restart_ports(target=self.target))
    
#---------------------------------------------------------------
#------------------- Complex thread tests ----------------------
#---------------------------------------------------------------

class moxa_sw_complex_thread(complex_thread):
    test_name = "SW MOXA complex thread test"
    test_desc = ""
    
    def __new__(cls, **parameters):
        if parameters.get('target') is not None:
            inst = complex_thread.__new__(cls, target=parameters['target'])
        else: inst = complex_thread.__new__(cls, target=sw_moxa(**parameters))
        return inst
    
    def __init__(self, **parameters):
        complex_thread.__init__(self, name=self.test_name + " " + self.target.ip, **parameters)    
        self.append('moxa_sw_test_restart_ports', moxa_sw_test_restart_ports(target=self.target))
