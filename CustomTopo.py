#!/usr/bin/python

'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2
Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1={}, linkopts2={}, linkopts3={}, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
        self.fanout = fanout
        
        #add coreSwitch
        coreSwitch = self.addSwitch( 's1')
        
        #add aggregation
        for i in range( 1, self.fanout+1):
            aggregationSwitch = self.addSwitch('s%s' %(1+i))
            self.addLink( coreSwitch, aggregationSwitch, **linkopts1)
            for j in range( 1,self.fanout+1):
                edgeSwitchNum = 1+ self.fanout*i + j
                edgeSwitch = self.addSwitch('s%s' %edgeSwitchNum)
                self.addLink( aggregationSwitch, edgeSwitch, **linkopts2)
                for k in range( 1,self.fanout+1):
                    hostNum = k+self.fanout*(j-1)+self.fanout*self.fanout*(i-1)
                    host = self.addHost('h%s' %hostNum)
                    self.addLink(edgeSwitch, host, **linkopts3)
                    
topos = { 'custom': ( lambda: CustomTopo() ) }

def simpleTest():
   "Create and test a simple network"
   fanout=input("fanout=?")
   topo = CustomTopo(fanout=fanout)
   net = Mininet(topo)
   net.start()
   print "Dumping host connections"
   dumpNodeConnections(net.hosts)
   print "Testing network connectivity"
   net.pingAll()
   net.stop()

if __name__ == '__main__':
   # Tell mininet to print useful information
   setLogLevel('info')
   simpleTest()
