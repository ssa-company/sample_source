# Tests HASP.
# We stop/start HASP key service

from common.service.service import service_control

from common.utils import logger

class hasp(service_control):
    def __init__(self):
        service_control.__init__(self, 'aksusbd')
        logger.debug("Init HASP service")