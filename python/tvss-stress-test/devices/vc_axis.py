# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import sys
import httplib

from base64 import b64encode

from common.utils import logger

from common.device.vc import vc
import common.utils as utils

class vc_axis(vc):
    __conn = None
    __headers_auth = None
    
    def __init__(self, **params):
        logger.debug("Init axis %s", params['ip'])
        vc.__init__(self, **params)
        auth = '%s:%s' % (self.user, self.password)
        auth = auth.encode('ascii') 
        userAndPass = b64encode(auth).decode("ascii")
        self.__headers_auth = {'Authorization' : 'Basic %s' % userAndPass }
            
        logger.debug("Connection string http://%s:%s@%s" % (self.user, self.password, self.ip))               
        try:   
            self.__conn = httplib.HTTPConnection("%s" % self.ip)
        except httplib.HTTPException as e:
            logger.error("Execution failed: %s", e)
            
    def __del__(self):
        self.__conn.close()
        vc.__del__(self)
    
    def restart(self):
        if vc.restart(self) == False: return
        try:
            self.__conn.request("GET", "/axis-cgi/restart.cgi", headers=self.__headers_auth)
            res = self.__conn.getresponse()
            #logger.debug("%s %s", res.status, res.reason)
        except httplib.HTTPException as e:
            logger.error("Execution failed: %s", e)    
    
    def set_parameter(self, param, value):
        try:
            self.__conn.request("GET", "/axis-cgi/param.cgi?action=update&%s=%s" % (param, value), headers=self.__headers_auth)
            res = self.__conn.getresponse()
            #logger.debug("%s %s", res.status, res.reason)
        except httplib.HTTPException as e:
            logger.error("Execution failed: %s", e) 
    
    def get_parameter(self, param):
        if utils.check_hostname(self.ip) == 1: return
        try:
            self.__conn.request("GET", "/axis-cgi/param.cgi?action=list&group=%s" % (param), headers=self.__headers_auth)
            res = self.__conn.getresponse()
            #logger.debug("%s %s", res.status, res.reason)
            data = res.read()
            return (data.split("=")[1]).strip()
        except httplib.HTTPException as e:
            logger.error("Execution failed: %s", e) 
            
    def disable_rtsp(self):
        if vc.disable_rtsp(self) == False: return
        self.set_parameter("Network.RTSP.Enabled", "no")
    
    def enable_rtsp(self):
        if vc.enable_rtsp(self) == False: return
        self.set_parameter("Network.RTSP.Enabled", "yes")
