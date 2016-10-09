#!/usr/bin/python
# -*- coding: utf8 -*-

# Main test file.
#
# List of tests:
# - hasp tests
# - storage space tests
# - lost vc tests
# - lost switch tests
# - combination all tests
#

import logging
import argparse
import sys
import time
import signal

import checks
import common.utils as utils
from common.utils import logger
from common.test.test_list import test_list
from common.daemon import daemon

import tvss_user_conf

class test_daemon(daemon):
    def run(self):
        test_code()

df_topology = 'tvss_topology.cfg'
df_config_root= '/opt/tvss/etc'

verbose = False
list_tests = False
daemon = False

d = None # Our daemon

tests = test_list("Tvss tests")

config_root = df_config_root

def parse_arguments():
    global config_root
    global topology_file
    global verbose
    global daemon
    global list_tests

    parser = argparse.ArgumentParser(description='TVSS test tool')

    parser.add_argument('--verbose', dest='verbose',
                        action='store_true', default=False,
                        help='verbose')
    
    parser.add_argument('--config_root', dest='config_root',
                        action='store', default=df_config_root,
                        help='tvs config files location')    
                        
    parser.add_argument('--list_tests', dest='list_tests',
                        action='store_true', default=False,
                        help='print list of tests')     
    
    parser.add_argument('--daemon', dest='daemon',
                        action='store_true', default=False,
                        help='run as daemon')                         
    
    args = parser.parse_args()

    config_root = args.config_root
    verbose = args.verbose
    daemon = args.daemon
    list_tests = args.list_tests
    

def end_test():
#---------------------------------------------------------------
#--------------------- RESTORE STATE SYSTEM --------------------
#---------------------------------------------------------------
        tests.return_init_state()
        if d is not None: d.delpid()
        sys.exit(0)

def signal_handler(signum, frame):
    global test_list
    
    if (signum == signal.SIGINT):
        logger.info('Application terminated by user')
        end_test()
    if (signum == signal.SIGTERM):
        logger.info('Application terminated by kill command')
        end_test()
          
def test_code():
    global tests
    # Enable debug message 
    # Default info
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        fmt = logging.Formatter(utils.FORMAT_DBG)
        utils.hndlr.setFormatter(fmt)
        fmt = logging.Formatter("%(asctime)-15s " + utils.FORMAT_DBG)
        utils.filehndlr.setFormatter(fmt)
    else:
        logging.getLogger().setLevel(logging.INFO)
        fmt = logging.Formatter(utils.FORMAT_INFO)
        utils.hndlr.setFormatter(fmt)
        fmt = logging.Formatter("%(asctime)-15s " + utils.FORMAT_INFO)
        utils.filehndlr.setFormatter(fmt)
        
    # Posix handler
    signal.signal(signal.SIGINT, signal_handler)   
    signal.signal(signal.SIGTERM, signal_handler)  
     
#---------------------------------------------------------------        
#-------------------- PRINT AVAILIBLE TESTS -------------------- 
#---------------------------------------------------------------               
    if list_tests:
        print("Availible tests:")
        for key in sorted(checks.tests_list.keys()):
            if hasattr(checks.tests_list[key], 'test_desc'):
                print("*** %-30s *** Description: %s" % (key, checks.tests_list[key].test_desc))
            else: print("*** %-30s ***" % (key))
        return
#---------------------------------------------------------------        
#-------------------------- ADD TESTs -------------------------- 
#---------------------------------------------------------------   
    
    logger.info('Loading User tests')
    tvss_user_conf.user_conf()

#---------------------------------------------------------------        
#-------------------------- RUN TESTs -------------------------- 
#---------------------------------------------------------------   

    logger.info('Start test TVSS')
    tests.run()
    
    # Application loop
    while True: time.sleep(0.1)   
        
def main(): 
    global d
    parse_arguments()
    
    if daemon:
        d = test_daemon("/var/run/tvss_test.pid")
        d.start()
        sys.exit(0)
    else:
        test_code()
        
if __name__ == '__main__':
    sys.exit(main())
