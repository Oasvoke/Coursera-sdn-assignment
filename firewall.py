'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''
import csv


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''
        with open(policyFile) as csvfile:
            rows = csv.DictReader(csvfile)
            for row in rows:
                # get mac address
                mac_0 = EthAddr(row['mac_0'])
                mac_1 = EthAddr(row['mac_1'])
                
                # create 2 match that cover both direction
                match1 = of.ofp_match()
                match1.dl_src = mac_0
                match1.dl_dst = mac_1
                
                match2 = of.ofp_match()
                match2.dl_src = mac_1
                match2.dl_dst = mac_0
                
                # create 2 massage that tell the switch do nothing if see match packet
                msg1 = of.ofp_flow_mod()
                msg2 = of.ofp_flow_mod()
                
                msg1.match = match1
                msg2.match = match2
                
                #send the firewall policy msg to switch if connected
                event.connection.send(msg1)
                event.connection.send(msg2)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
