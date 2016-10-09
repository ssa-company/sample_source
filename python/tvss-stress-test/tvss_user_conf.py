#!/usr/bin/python
# -*- coding: utf8 -*-

import tvss_test
import os
import json

from devices import *
from common.utils import logger

switches = {}

def tests_from_topo(config_root, topo_fname):
    topology_file = config_root + '/' + topo_fname
    logger.info("Load topology file %s" % topology_file)
    if not os.path.exists(topology_file):
        logger.warning("Can't open tvss_topology.cfg")
        return
    
    # Open topology file
    fd_topo = open(topology_file, 'r')
    __topology = json.load(fd_topo)
    logger.info("Load devices from topology")
    for sw_obj in __topology['devices']:
        # Check sw
        if not sw_obj.get('errors'):
            if switches.get(sw_obj['id']) is not None:
                sw = sw_moxa.sw_moxa(mac=sw_obj['id'], ip=sw_obj['ip_address'], name=sw_obj['location'], user="admin", password="2OD4%g5Uh8", snmp_rw_pass="klg3zaNJyTEp", ports=switches.get(sw_obj['id']))
                if sw is not None:
#                    tvss_test.tests.append("SW MOXA test restart", target=sw)
#                    tvss_test.tests.append("SW MOXA complex test", target=sw)
                    tvss_test.tests.append("SW MOXA complex thread test", target=sw, min_sleep=120, max_sleep=180)
                    for vc_obj in sw_obj['vc']:
                        if vc_obj['name'] != "VC99":
                            # Check vc
                            vc = vc_axis.vc_axis(mac=vc_obj['id'] , ip=vc_obj['ip_address'], name=vc_obj['name'], user="root", password="L1811%h3eR", snmp_rw_pass="klg3zaNJyTEp")
                            if vc is not None: 
#                                tvss_test.tests.append("VC AXIS test restart", target=vc)
#                                tvss_test.tests.append("VC AXIS test RTSP", target=vc)
#                                tvss_test.tests.append("VC AXIS test UDP", target=vc)
                                tvss_test.tests.append("VC AXIS complex thread test", target=vc, min_sleep=120, max_sleep=180)

    # Close topology file
    fd_topo.close()  

def user_conf():
    global switches
    # Перечень коммутаторов и портов, на которых проводятся тесты
    switches['00-90-E8-44-FE-AA'] = ['1', '2', '3']
    switches['00-90-E8-42-F9-0B'] = ['1', '2', '3']
    switches['00-90-E8-2D-BC-E2'] = ['1', '2', '3']
    switches['00-90-E8-2E-19-E9'] = ['1', '2', '3']
    
    tests_from_topo(tvss_test.config_root, tvss_test.df_topology)
    
    # Create HASP test
    tvss_test.tests.append("Hasp complex thread test", min_sleep=120, max_sleep=240)

    
    
