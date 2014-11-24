#!/bin/bash

# Justin Mammarella 24/11/2014
# The script will scan OpenStack compute nodes and report on their current resource usage.
#
# Information pertaining to VMs is gathered using NOVA commands. From this, VM flavour and state is obtained.
# Physical information about node hardware is obtained by examining /proc/cpuinfo /proc/meminfo on nodes via ssh.

# A file containg a list of all node hostnames must be provided.
# Hosts must be accessible via SSH and keys verified.


rm -f ./flavors
rm -f ./tmp

HOST=np-rcc50

#Retrieve Flavour information 

nova flavor-list | tail -n 6 | head -n 5 >> tmp

#Store Flavour Infomration in memory for retrieval later

cat tmp | while read line; do
    var=$(echo $line | cut -f3 -d'|' | tr -d ' ' | tr -d '.' )
    mem=$(echo $line | cut -f4 -d'|' | tr -d ' ' | tr -d '.' )
    cpu=$(echo $line | cut -f8 -d'|' | tr -d ' ' | tr -d '.' )
    echo "$var $mem $cpu" >> flavors
done 


#For Each Host get VM information:

hostlist='/home/jmammarella/openstack/nodes/np-rcc'

exec 3<$hostlist

while read -u3 HOST; do

    totalcores=0
    totalmem=0

    rm -f ./tmp3
    rm -f ./tmp2
    rm -f ./tmp4
    rm -f ./tmp5
    
    #For Each VM calculate resource usage.

    #nova list --host np-rcc5 --all-tenants

    #Get a list of VMs running on the Node.
    
    nova list --host $HOST --all-tenants >> tmp2
    n=`expr $(cat tmp2 | wc -l) - 3`
    cat tmp2 | tail -n $n | head -n -1 >> tmp3

    filename='tmp3'
    exec 4<$filename

    #Itterate over VM list of Nodes, extracting ID and State.

    while read -u4 line; do

        id=$(echo $line | cut -f2 -d '|') 
        
        nova show $id > tmp6

        flav=`cat tmp6 | grep flavor | cut -f3 -d'|' | cut -f1 -d'(' | tr -d ' ' | tr -d '.'`
        state=`cat tmp6 | grep vm_state | cut -f3 -d'|' | tr -d ' '`
        
        #Use flavor information to determine number of cores and memory reserved for VMs.

        if [ "$state" != "suspended" ]; then 

            # cat flavors | grep $flav
            mem=$(cat flavors | grep $flav | cut -f2 -d' ' | tr -d ' ' )  
            cores=$(cat flavors | grep $flav | cut -f3 -d' ' | tr -d ' ')  
    
            totalcores=`expr $cores + $totalcores`
            totalmem=`expr $mem + $totalmem`
        fi

    done

    vm_count=`expr $(cat tmp2 | wc -l) - 4`

    echo "========================================="
    echo "Host: $HOST"
    echo "========================================="
    echo "Number of VMs: $vm_count"
    echo "Total Cores In Use/Reserved: $totalcores || Total Mem Reserverd By VMs: $totalmem MB"

    ssh $HOST "cat /proc/cpuinfo" >> tmp4

    #Count Physical CPU Cores.

    filename='tmp4'
    exec 5<$filename
    cores=0
    while read -u5 line; do
        
        if [ "$(echo $line | cut -f1 -d':' | tr -d ' ')" = "cpucores" ]; then
                cores=`expr $cores + $(echo $line | cut -f2 -d':' | tr -d ' ')`  

        fi
    done

    #Get Physical Memory
    
    ssh $HOST "cat /proc/meminfo" >> tmp5

    sys_memfree=`expr $(cat tmp5 | grep MemFree: | cut -f2 -d':' | tr -d ' ' | tr -d 'kB') / 1024`
    sys_memtotal=`expr $(cat tmp5 | grep MemTotal: | cut -f2 -d':' | tr -d ' ' | tr -d 'kB') / 1024`

    echo "Total Cores on Host: $cores || Total Mem Avail on Host:$sys_memtotal MB - Current System Mem Free: $sys_memfree MB"
    echo "--"
    echo "Free Cores: $(expr $cores - $totalcores) || Mem Available for New VMs = $(expr $sys_memtotal - $totalmem) MB"
    #rm flavors

done

