# Common utils.

import os
import random
import time
import subprocess
from subprocess import call 
import logging

FORMAT_DBG = "%(levelname)-7s **: (%(filename)s:%(lineno)s:%(funcName)s) - %(message)s"
FORMAT_INFO = "%(levelname)-7s **: %(message)s"

# Loggers
logging.basicConfig()
logger = logging.getLogger()
hndlr = logger.handlers[0]
filehndlr = logging.FileHandler("tvss_test.log")
logger.addHandler(filehndlr)

def random_sleep(min, max):
    timeout = random.randint(min, max)
    logger.debug("Random timeout %s", timeout)
    time.sleep(timeout)

def random_true():
    res = random.randint(0, 1)
    return res

def check_hostname(hostname):
    FNULL = open(os.devnull, 'w')
    res = call("ping %s -c 1" % (hostname), stdout = FNULL, stderr = subprocess.STDOUT, shell=True) 
    # logger.debug("Res %s" % res)
    return res