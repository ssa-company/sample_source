# Device class

import common.utils as utils
from common.utils import logger

class device(object):
    __mac = None
    __ip = None
    __name = None
    __user = None
    __password = None
    __snmp_rw_pass = None
    
    def __new__(cls, **params):
        res = utils.check_hostname(params['ip'])
        if res == 1:
            logger.warning("Host %s not answer" % (params['ip']))
            logger.error("Device not created")
            return None
        return object.__new__(cls)  
    
    def __init__(self, **params):
        self.__mac = params['mac']
        self.__ip = params['ip']
        self.__name = params['name']
        self.__user = params['user']
        self.__password = params['password']
        self.__snmp_rw_pass = params['snmp_rw_pass']
        
    def __del__(self):
        pass
    
    @property
    def ip(self):
        return self.__ip
    
    @property
    def mac(self):
        return self.__mac
    
    @property
    def name(self):
        return self.__name
    
    @property
    def user(self):
        return self.__user
    
    @property
    def password(self):
        return self.__password
    
    @property
    def snmp_rw_pass(self):
        return self.__snmp_rw_pass

