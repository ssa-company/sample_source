#!/usr/bin/python
# -*- coding: utf8 -*-

# Test VC

import sys, inspect
import common.utils as utils
from common.utils import logger
from common.test.simple import simple
from common.test.complex import complex
from common.test.complex_thread import complex_thread

from devices.vc_axis import vc_axis

#---------------------------------------------------------------
#----------------------- Simple tests --------------------------
#---------------------------------------------------------------

class axis_vc_test_restart(simple):
    test_name = "VC AXIS test restart"
    test_desc = "Тест для перезагрузки камеры"
    
    def __new__(cls, **parameters):
        if parameters.get('target') is not None:
                inst = simple.__new__(cls, target=parameters['target'])
        else: inst = simple.__new__(cls, target=vc_axis(**parameters))
        return inst
        
    def __init__(self, **parameters):
        simple.__init__(self, name=self.test_name + " " + self.target.ip)     
        
    def save_init_state(self):
        simple.save_init_state(self)
    
    def return_init_state(self):
        if self._runned == False: return
        simple.return_init_state(self) 
        
    def handler(self):
        simple.handler(self)
        if (utils.random_true()): self.target.restart()
                
class axis_vc_test_rtsp(simple):
    test_name = "VC AXIS test RTSP"
    test_desc = "Тест для отключения/включения RTSP на камере"
    
    def __new__(cls, **parameters):
        if parameters.get('target') is not None:
                inst = simple.__new__(cls, target=parameters['target'])
        else: inst = simple.__new__(cls, target=vc_axis(**parameters))
        return inst
        
    def __init__(self, **parameters):
        simple.__init__(self, name=self.test_name + " " + self.target.ip)     
        
    def save_init_state(self):
        simple.save_init_state(self)
        n = {"RTSP" : self.target.get_parameter("Network.RTSP.Enabled")} 
        self.init_state.update(n) 
        
    def return_init_state(self):
        if self._runned == False: return
        simple.return_init_state(self) 
        if self.init_state["RTSP"] == "no": 
            self.target.disable_rtsp()
        elif self.init_state["RTSP"] == "yes": 
            self.target.enable_rtsp()
        
    def handler(self):
        simple.handler(self)
        if (utils.random_true()): self.target.disable_rtsp()
        else: self.target.enable_rtsp()    
        
class axis_vc_test_udp(simple):
    test_name = "VC AXIS test UDP"
    test_desc = "Тест блокирующий UDP пакеты от камеры"
    
    def __new__(cls, **parameters):
        if parameters.get('target') is not None:
                inst = simple.__new__(cls, target=parameters['target'])
        else: inst = simple.__new__(cls, target=vc_axis(**parameters))
        return inst
        
    def __init__(self, **parameters):
        simple.__init__(self, name=self.test_name + " " + self.target.ip)     
    
    def save_init_state(self):
        if self._runned == False: return
        simple.save_init_state(self)
        n = {"DROP_UDP" : self.target.check_rule(self.target.drop_udp_rule())} 
        self.init_state.update(n)
        
    def return_init_state(self):
        simple.return_init_state(self) 
        rule = self.target.drop_udp_rule()
        if self.check_rule(rule):
            if self.init_state["DROP_UDP"] == True: self.target.add_rule(rule)
            else: self.target.remove_rule(rule)
    
    def handler(self):
        simple.handler(self)
        if (utils.random_true()): self.target.add_rule(self.target.drop_udp_rule())
        else: self.target.remove_rule(self.target.drop_udp_rule())
        
#---------------------------------------------------------------
#---------------------- Complex tests --------------------------
#---------------------------------------------------------------

class axis_vc_complex(complex):      
    test_name = "VC AXIS complex test"
    test_desc = "Комплексный тест камеры AXIS"
    
    def __new__(cls, **parameters):
        if parameters.get('target') is not None:
            inst = complex.__new__(cls, target=parameters['target'])
        else: inst = complex.__new__(cls, target=sw_moxa(**parameters))
        return inst
    
    def __init__(self, **parameters):
        complex_thread.__init__(self, name=self.test_name + " " + self.target.ip)    
        self.append('axis_vc_test_restart', axis_vc_test_restart(target=self.target))
        self.append('axis_vc_test_rtsp', axis_vc_test_rtsp(target=self.target))
        self.append('axis_vc_test_udp', axis_vc_test_udp(target=self.target))
    
#---------------------------------------------------------------
#------------------- Complex thread tests ----------------------
#---------------------------------------------------------------

class axis_vc_complex_thread(complex_thread):
    test_name = "VC AXIS complex thread test"
    test_desc = "Комплексный циклический тест камеры AXIS"
    
    def __new__(cls, **parameters):
        if parameters.get('target') is not None:
            inst = complex_thread.__new__(cls, target=parameters['target'])
        else: inst = complex_thread.__new__(cls, target=vc_axis(**parameters))
        return inst
    
    def __init__(self, **parameters):
        complex_thread.__init__(self, name=self.test_name + " " + self.target.ip, **parameters)  
        self.append('axis_vc_test_restart', axis_vc_test_restart(target=self.target))
        self.append('axis_vc_test_rtsp', axis_vc_test_rtsp(target=self.target))
#        self.append('axis_vc_test_udp', axis_vc_test_udp(target=self.target))

    