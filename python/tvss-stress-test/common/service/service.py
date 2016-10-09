#!/usr/bin/python
# -*- coding: utf8 -*-

# Service utils.

import os, sys
import shlex, subprocess
from subprocess import call 
from enum import Enum

from common.utils import logger

class Service_State(Enum):
    run = 1
    stop = 2
    unknown = 3
    
class service_control(object):
    __service_name = None
    __state = Service_State.unknown
    
    @property
    def service_name(self):
        return self.__service_name
    
    @property    
    def state(self):
        try:
            logger.debug("%s: Check service state", self.service_name)
            FNULL = open(os.devnull, 'w')
            retcode = call("pgrep %s" % (self.service_name), stdout = FNULL, stderr = subprocess.STDOUT, shell=True) 
            if retcode == 0:
                logger.info("%s: Service runnig" % (self.service_name))
                return Service_State.run
            else: 
                logger.info("%s: Service stopped" % (self.service_name))    
                return Service_State.stop
        except OSError as e:
            logger.error("Execution failed: %s", e)
        
    def __init__(self, service_name):
        self.__service_name = service_name
        self.__state = Service_State.unknown
        logger.debug("Init service object")
            
    def start(self):
        try:
            retcode = call("service %s %s" % (self.service_name, "start"), shell=True)
            if retcode < 0:
                logger.error("%s: Unable start the service" % (self.service_name))
            elif retcode == 0:
                logger.info("%s: Service is started succesfully" % (self.service_name))
                self.__state = Service_State.run
            else:
                logger.warning("Service already started")
        except OSError as e:
            logger.error("Execution failed: %s", e)

    def stop(self):
        try:
            retcode = call("service %s %s" % (self.service_name, "stop"), shell=True)
            if retcode < 0:
                logger.error("%s: Unable stop the service" % (self.service_name))
            elif retcode == 0:
                logger.info("%s: Service is stopped succesfully" % (self.service_name))
                self.__state = Service_State.stop
            else:
                logger.warning("%s: Service already stopped" % (self.service_name))
        except OSError as e:
            logger.error("Execution failed: %s", e )

    def restart(self):
        self.stop_service()
        self.start_services()            
            
    def state_str(self):
        if self.__state == Service_State.unknown:
            logger.info("%s: Service state unknown" % (self.service_name))
        elif self.__state == Service_State.run:   
            logger.info("%s: Service running" % (self.service_name))
        elif self.__state == Service_State.stop:   
            logger.info("%s: Service stopped" % (self.service_name))    