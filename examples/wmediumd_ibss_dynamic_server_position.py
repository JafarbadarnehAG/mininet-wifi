#!/usr/bin/python

"""
This example shows how to use the wmediumd connector to prevent mac80211_hwsim stations reaching each other
(Position previously defined)

It starts the wmediumd and 'disables' the connection from sta1 to sta2

authors: Patrick Grosse (patrick.grosse@uni-muenster.de)
         Ramon Fontes (ramonrf@dca.fee.unicamp.br)
"""

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.wmediumdConnector import WmediumdStarter, DynamicWmediumdIntfRef, WmediumdLink, WmediumdServerConn


def topology():
    """Create a network. sta1 <--> sta2 <--> sta3"""

    print "*** Network creation"
    net = Mininet()

    print "*** Creating nodes"
    sta1 = net.addStation('sta1', range=50, position='10,10,0')
    sta2 = net.addStation('sta2', range=50, position='20,10,0')
    sta3 = net.addStation('sta3', range=50, position='30,10,0')

    print "*** Configure wmediumd"
    # This should be done right after the station has been initialized
    sta1.wmediumdIface = DynamicWmediumdIntfRef(sta1)
    sta2.wmediumdIface = DynamicWmediumdIntfRef(sta2)
    sta3.wmediumdIface = DynamicWmediumdIntfRef(sta3)

    intfrefs = [sta1.wmediumdIface, sta2.wmediumdIface, sta3.wmediumdIface]
    links = [
        WmediumdLink(sta1.wmediumdIface, sta2.wmediumdIface, 15),
        WmediumdLink(sta2.wmediumdIface, sta1.wmediumdIface, 15),
        WmediumdLink(sta2.wmediumdIface, sta3.wmediumdIface, 15),
        WmediumdLink(sta3.wmediumdIface, sta2.wmediumdIface, 15)]
    WmediumdStarter.initialize(intfrefs, links, with_server=True)

    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    print "*** Start wmediumd"
    WmediumdStarter.start()

    print "*** Plotting graph ***"
    net.plotGraph(max_x=200, max_y=200)

    print "*** Enabling Mesh Routing ***"
    net.meshRouting('custom')

    print "*** Creating links"
    net.addMesh(sta1, ssid='adNet')
    net.addMesh(sta2, ssid='adNet')
    net.addMesh(sta3, ssid='adNet')

    print "*** Starting network"
    net.start()
    print "\n\n\n"
    print "*** Pinging sta2"
    sta1.cmdPrint('ping -c 1 10.0.0.2')

    print "*** Update wmediumd"
    WmediumdServerConn.connect()

    # Required when the position of the nodes are previously defined. Useful to set channel params.
    net.autoAssociation()

    CLI(net)

    print "*** Stopping network"
    net.stop()

    print "*** Stopping wmediumd"
    WmediumdServerConn.disconnect()
    WmediumdStarter.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
