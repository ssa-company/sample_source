# Common class for test

from common.utils import logger

class test(object):
    __name = None
    __init_state = {}
    __run_handler = None
    __target_obj = None
    _runned = False
    
    def __new__(cls, **parameters):
        if parameters.get('target') is None: return None
        inst = object.__new__(cls)
        inst.__target_obj = parameters['target']
        return inst
    
    def __init__(self, **parameters):
        self.__name = parameters['name']
        self.__run_handler = self.handler
        self.__init_state = {}
        logger.debug("Init test \"%s\"", self.__name)
    
    @property
    def name(self):
        return self.__name
    
    @property
    def init_state(self):
        return self.__init_state
    
    @property
    def run_handler(self):
        return self.__run_handler
    
    @run_handler.setter
    def run_handler(self, value):
        self.__run_handler = value
        
    @property
    def target(self):
        return self.__target_obj
        
    def handler(self):
        logger.info("Run test \"%s\"" % (self.__name))

#---------------------------------------------------------------        
#------------------------- INIT STATE -------------------------- 
#---------------------------------------------------------------

    def save_init_state(self):
        logger.debug("Save init state test \"%s\"", self.__name)
        self._runned = True
        
    def return_init_state(self):    
        if self._runned == False: return
        logger.debug("Return init state test \"%s\"", self.__name)
        self._runned = False

#---------------------------------------------------------------        
#---------------------------- TESTs ---------------------------- 
#---------------------------------------------------------------

    def run(self):
        if self._runned == True: return
        self.save_init_state()
        self.handler()
        self.return_init_state()
