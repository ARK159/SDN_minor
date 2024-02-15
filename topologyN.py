
# from time import sleep
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from datetime import datetime
from random import randrange, choice
from time import sleep

def ip_generator():
    ip = ".".join(["10","0","0",str(randrange(1,19))])
    return ip

def myNetwork():
    
    net = Mininet( topo=None,
                build=False,
                ipBase='10.0.0.0/24')
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    s1 = net.addSwitch( 's1', cls=OVSKernelSwitch, protocols='OpenFlow13' )

    h1 = net.addHost( 'h1',cpu=1.0/20,mac="00:00:00:00:00:01", ip="10.0.0.1/24" )
    h2 = net.addHost( 'h2',cpu=1.0/20, mac="00:00:00:00:00:02", ip="10.0.0.2/24" )
    h3 = net.addHost( 'h3',cpu=1.0/20, mac="00:00:00:00:00:03", ip="10.0.0.3/24" )    

    s2 = net.addSwitch( 's2', cls=OVSKernelSwitch, protocols='OpenFlow13' )

    h4 = net.addHost( 'h4',cpu=1.0/20, mac="00:00:00:00:00:04", ip="10.0.0.4/24" )
    h5 = net.addHost( 'h5',cpu=1.0/20, mac="00:00:00:00:00:05", ip="10.0.0.5/24" )
    h6 = net.addHost( 'h6',cpu=1.0/20, mac="00:00:00:00:00:06", ip="10.0.0.6/24" )

    s3 = net.addSwitch( 's3', cls=OVSKernelSwitch, protocols='OpenFlow13' )

    h7 = net.addHost( 'h7',cpu=1.0/20, mac="00:00:00:00:00:07", ip="10.0.0.7/24" )
    h8 = net.addHost( 'h8',cpu=1.0/20, mac="00:00:00:00:00:08", ip="10.0.0.8/24" )
    h9 = net.addHost( 'h9',cpu=1.0/20, mac="00:00:00:00:00:09", ip="10.0.0.9/24" )

    s4 = net.addSwitch( 's4', cls=OVSKernelSwitch, protocols='OpenFlow13' )

    h10 = net.addHost( 'h10',cpu=1.0/20, mac="00:00:00:00:00:10", ip="10.0.0.10/24" )
    h11 = net.addHost( 'h11',cpu=1.0/20, mac="00:00:00:00:00:11", ip="10.0.0.11/24" )
    h12 = net.addHost( 'h12',cpu=1.0/20, mac="00:00:00:00:00:12", ip="10.0.0.12/24" )

    s5 = net.addSwitch( 's5', cls=OVSKernelSwitch, protocols='OpenFlow13' )

    h13 = net.addHost( 'h13',cpu=1.0/20, mac="00:00:00:00:00:13", ip="10.0.0.13/24" )
    h14 = net.addHost( 'h14',cpu=1.0/20, mac="00:00:00:00:00:14", ip="10.0.0.14/24" )
    h15 = net.addHost( 'h15',cpu=1.0/20, mac="00:00:00:00:00:15", ip="10.0.0.15/24" )

    s6 = net.addSwitch( 's6', cls=OVSKernelSwitch, protocols='OpenFlow13' )

    h16 = net.addHost( 'h16',cpu=1.0/20, mac="00:00:00:00:00:16", ip="10.0.0.16/24" )
    h17 = net.addHost( 'h17',cpu=1.0/20, mac="00:00:00:00:00:17", ip="10.0.0.17/24" )
    h18 = net.addHost( 'h18',cpu=1.0/20, mac="00:00:00:00:00:18", ip="10.0.0.18/24" )

    # Add links

    net.addLink( h1, s1 )
    net.addLink( h2, s1 )
    net.addLink( h3, s1 )

    net.addLink( h4, s2 )
    net.addLink( h5, s2 )
    net.addLink( h6, s2 )

    net.addLink( h7, s3 )
    net.addLink( h8, s3 )
    net.addLink( h9, s3 )

    net.addLink( h10, s4 )
    net.addLink( h11, s4 )
    net.addLink( h12, s4 )

    net.addLink( h13, s5 )
    net.addLink( h14, s5 )
    net.addLink( h15, s5 )

    net.addLink( h16, s6 )
    net.addLink( h17, s6 )
    net.addLink( h18, s6 )

    net.addLink( s1, s2 )
    net.addLink( s2, s3 )
    net.addLink( s3, s4 )
    net.addLink( s4, s5 )
    net.addLink( s5, s6 )
    
    net.build()
    
    for switch in net.switches:
        switch.start([c0])
    
    CLI(net)
    net.stop()
    
    
if __name__ == '__main__':
    myNetwork()