# For drop test run 
# sudo aptitude install python3-setuptools
# sudo easy_install3 pip
# sudo python3 -m pip install --upgrade python-iptables

import iptc

from common.utils import logger
from device import device

import common.utils as utils

class vc(device):  
    chain = None
    
    def __new__(cls, **params):
        logger.debug("Create vc %s" % (params['name']))
        inst = device.__new__(cls, **params)
        return inst
        
    def __init__(self, **params):
        device.__init__(self, **params)
        self.chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        
    def __del__(self):
        device.__del__(self)    
        
    def restart(self):
        logger.info("Restart %s" % (self.name))
        if not utils.check_hostname(self.ip):
            print("Bad device")
            return False
        else:
            print("Good device")
            return True
        
    def disable_rtsp(self):
        logger.info("Disable RTSP at %s" % (self.name))
        if not utils.check_hostname(self.ip):
            return False
        else: return True
        
    def enable_rtsp(self):
        logger.info("Enable RTSP at %s" % (self.name))
        if not utils.check_hostname(self.ip):
            return False
        else: return True
            
    def drop_udp_rule(self):
        rule = iptc.Rule()
        rule.in_interface = "eth0"
        rule.src = self.ip
        rule.protocol = "udp"
        rule.target = iptc.Target(rule, "DROP")
        return rule
    
    def add_rule(self, rule):
        if not utils.check_hostname(self.ip):
            return False
        self.chain.insert_rule(rule)
        return True
    
    def remove_rule(self, rule):
        if not utils.check_hostname(self.ip):
            return False
        self.chain.delete_rule(rule) 
        return True
        
    def check_rule(self, rule):
        if not utils.check_hostname(self.ip):
            return False
        res = False
        for r in self.chain.rules:
            if r == rule: res = True
        return res    
