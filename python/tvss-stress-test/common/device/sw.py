# Test switch via telnet client

from device import device
from common.utils import logger

class sw(device):
    __ports = []
    
    @property
    def ports(self):
        return self.__ports
    
    def __new__(cls, **params):
        logger.debug("Create sw %s/%s" % (params['name'], params['ip']))
        inst = device.__new__(cls, **params)
        return inst
                
    def __init__(self, **params):
        device.__init__(self, **params)
        self.__ports = []
        if params['ports'] is not None: self.append_ports(params['ports'])
        
    def enter_cfg_mode(self):
        logger.info("%s: enter to cfg mode" % (self.name))
    
    def down_iff(self, id_iff):
        logger.info("Disable at %s/%s port %s" % (self.name, self.ip, id_iff))
     
    def up_iff(self, id_iff):
        logger.info("Enable at %s/%s port %s" % (self.name, self.ip, id_iff))    
    
    def append_port(self, id):
        logger.debug("Append port %s to sw %s/%s" % (id, self.name, self.ip))
        self.__ports.append(id)
        
    def append_ports(self, ids):
        for id in ids:
            self.append_port(id)

    def check_iif_state(self, id_iff):
        pass
    
