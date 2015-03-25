#!/bin/bash
#Script adapted from commands at: http://lartc.org/howto/lartc.rpdb.multiple-links.html
#Justin Mammarella 13/03/2015

T1=vlan3016
IF1=br-ex
P1_NET=172.26.40.0/21
#Gateway
P1=172.26.40.1
#CHANGE ME
IP1=172.26.40.17
NETMASK1=255.255.248.0

T2=vlan856
IF2=eth1
P2_NET=172.26.8.0/24
#Gateway
P2=172.26.8.1
#CHANGE ME
IP2=172.26.8.163


#Create the Ports to br-ex if they don't exist

if ! $(ovs-vsctl br-exists br-ex); then 
        if [ '$(ovs-vsctl list-ports br-ex | grep eth4)' ]; then
                echo "Creating port br-ex eth4"
                sudo ovs-vsctl add-port br-ex eth4
        fi

elif
        echo "Damn.. no ovs-vsctl bridge br-ex exists.."
fi

#Configure the IP Addresses of the interfaces

ifconfig eth4 0.0.0.0 netmask 0.0.0.0
ifconfig br-ex $IP1 netmask $NETMASK1

#Set the MTUs to fix bug with ssh connections and to allow better throughput for fast connections.

ifconfig br-ex mtu 9000 up
ifconfig eth1 mtu 1500 up
ifconfig eth4 mtu 9000 up


#Add the new routing tables

if [ -z "`cat /etc/iproute2/rt_tables | grep $T1`" ]; then
    echo "1 $T1" >> /etc/iproute2/rt_tables
fi

if [ -z "`cat /etc/iproute2/rt_tables | grep $T2`" ]; then
    echo "2 $T2" >> /etc/iproute2/rt_tables
        
fi

#Configure routing tables

ip route flush table $T1
ip route add $P1_NET dev $IF1 src $IP1 table $T1
ip route add default via $P1 table $T1

ip route show table $T1

ip route flush table $T2
ip route add $P2_NET dev $IF2 src $IP2 table $T2
ip route add default via $P2 table $T2

ip route show table $T2

#Setup main routes

ip route add $P1_NET dev $IF1 src $IP1
ip route add $P2_NET dev $IF2 src $IP2

#Add default routes (We dont need this)
#ip route add default via $P1


#Setup Routing Rules

if [ -z "`ip rule list | grep $T1`" ]; then
         ip rule add from $IP1 table $T1
fi

if [ -z "`ip rule list | grep $T2`" ]; then
        ip rule add from $IP2 table $T2
fi
ip rule list

