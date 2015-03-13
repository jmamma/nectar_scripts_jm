#!/bin/bash
#Script adapted from commands at: http://lartc.org/howto/lartc.rpdb.multiple-links.html
#Justin Mammarella 13/03/2015

T1=vlan3016
IF1=eth4
P1_NET=172.26.40.0/21
#Gateway
P1=172.26.40.1
#CHANGE ME
IP1=172.26.40.16

T2=vlan856
IF2=eth1
P2_NET=172.26.8.0/24
#Gateway
P2=172.26.8.1
#CHANGE ME
IP2=172.26.8.161


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

