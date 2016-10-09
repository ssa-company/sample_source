import telnetlib
import netsnmp
import time

from common.device.sw import sw

from common.utils import logger

class sw_moxa(sw): 
    __tn = None
    
    def enter_cfg_mode(self):
        sw.enter_cfg_mode(self)
        self.__tn = telnetlib.Telnet(self.ip) 
        try:    
            self.__tn.read_until("login as: ".encode(), 5)
            self.__tn.write(self.user.encode() + "\n".encode())
        except EOFError as e:
            logger.error("%s: Execution failed: %s" % (self.ip, e))
            return
        
        if self.password:
            try:
                self.__tn.read_until("password: ".encode(), 5)
                self.__tn.write(self.password.encode() + "\n\n".encode())
            except EOFError as e:
                logger.error("%s: Execution failed: %s" % (self.ip, e))
                return    
       
        try:
            self.__tn.write("configure\n".encode())
        except EOFError as e:
            logger.error("%s: Execution failed: %s" % (self.ip, e))
            return
        
    def exit_cfg_mode(self):
        try:
            self.__tn.write("exit\n".encode())
            self.__tn.write("exit\n".encode())
        except EOFError as e:
            logger.error("%s: Execution failed: %s" % (self.ip, e))
            return
        # timeout for correct work telnet
        time.sleep(1) 
    
    def up_iff(self, id_iff):
        sw.up_iff(self, id_iff)
        
        var=netsnmp.Varbind('.1.3.6.1.4.1', '8691.7.19.1.9.1.1.3.%s' % id_iff, '1', 'INTEGER')
        netsnmp.snmpset(var,Version=2,Community=self.snmp_rw_pass,DestHost=self.ip)
        
#        self.enter_cfg_mode()
#        request = "interface ethernet %s\n" % (id_iff)
#        try:
#            self.__tn.write(request.encode())
#            self.__tn.write("no shutdown\n".encode())
#            self.__tn.write("exit\n".encode())
#        except EOFError as e:
#            logger.error("%s: Execution failed: %s" % (self.ip, e))
#            return
#        self.exit_cfg_mode()
    
    def down_iff(self, id_iff):
        sw.down_iff(self, id_iff)
        
        var=netsnmp.Varbind('.1.3.6.1.4.1', '8691.7.19.1.9.1.1.3.%s' % id_iff, '0', 'INTEGER')
        netsnmp.snmpset(var,Version=2,Community=self.snmp_rw_pass,DestHost=self.ip)
#    
#        self.enter_cfg_mode()
#        request = "interface ethernet %s\n" % (id_iff)
#        try:
#            self.__tn.write(request.encode())
#            self.__tn.write("shutdown\n".encode())
#            self.__tn.write("exit\n".encode())
#        except EOFError as e:
#            logger.error("%s: Execution failed: %s" % (self.ip, e))
#            return
#        self.exit_cfg_mode()
        
    def check_iif_state(self, id_iff):
        logger.debug("Check iif %s from %s", id_iff, self.ip)
        res = True
        
        snmp_res = netsnmp.snmpget('.1.3.6.1.4.1.8691.7.19.1.9.1.1.3.' + id_iff, Version=2, Community=self.snmp_rw_pass, DestHost=self.ip)
        if snmp_res[0] == 0: res = False
#        self.__tn = telnetlib.Telnet(self.ip) 
#        try:
#            self.__tn.read_until("login as: ".encode(), 5)
#        except EOFError as e:
#            logger.error("%s: Execution failed: %s" % (self.ip, e))
#            return
#            
#        try:     
#            self.__tn.write(self.user.encode() + "\n".encode())
#        except EOFError as e:
#            logger.error("%s: Execution failed: %s" % (self.ip, e))
#            return
#        
#        if self.password:
#            try:
#                self.__tn.read_until("password: ".encode(), 5)
#                return
#            except EOFError as e:
#                logger.error("%s: Execution failed: %s" % (self.ip, e))
#                return
#                
#            try:    
#                self.__tn.write(self.password.encode() + "\n\n".encode())
#            except EOFError as e:
#                logger.error("%s: Execution failed: %s" % (self.ip, e))
#        
#        request = "show interfaces ethernet %s\n" % (id_iff)
#        self.__tn.write(request.encode())
#        self.__tn.write("exit\n".encode())
#        str = self.__tn.read_all().decode()
#        if ("Enable" in str):
#            res = True
#        elif ("Disable" in str):
#            res = False
#        
        return res

        