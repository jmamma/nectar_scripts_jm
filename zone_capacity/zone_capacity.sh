#!/bin/bash

rm ./tmp
rm ./tmp3
rm ./tmp2
rm ./tmp4
rm ./tmp5
rm ./flavors
HOST=np-rcc9
totalcores=0
totalmem=0

nova flavor-list | tail -n 6 | head -n 5 >> tmp

#Store Flavour Infomration in memory

cat tmp | while read line; do
    var=$(echo $line | cut -f3 -d'|' | tr -d ' ' | tr -d '.' )
    mem=$(echo $line | cut -f4 -d'|' | tr -d ' ' | tr -d '.' )
    cpu=$(echo $line | cut -f8 -d'|' | tr -d ' ' | tr -d '.' )
    echo "$var $mem $cpu" >> flavors
done 

#nova list --host np-rcc5 --all-tenants

nova list --host $HOST --all-tenants >> tmp2
n=`expr $(cat tmp2 | wc -l) - 3`
cat tmp2 | tail -n $n | head -n -1 >> tmp3

filename='tmp3'
exec 4<$filename

while read -u4 line; do

    id=$(echo $line | cut -f2 -d '|') 

    flav=`nova show $id | grep flavor | cut -f3 -d'|' | cut -f1 -d'(' | tr -d ' ' | tr -d '.'`
   # cat flavors | grep $flav
    mem=$(cat flavors | grep $flav | cut -f2 -d' ' | tr -d ' ' )  
    cores=$(cat flavors | grep $flav | cut -f3 -d' ' | tr -d ' ')  
    
    totalcores=`expr $cores + $totalcores`
    totalmem=`expr $mem + $totalmem`

done

echo "Host: $HOST TotalCoresInUseByVM: $totalcores TotalMemInUseByVM: $totalmem"

ssh $HOST "cat /proc/cpuinfo" >> tmp4


filename='tmp4'
exec 5<$filename
cores=0
while read -u5 line; do
        
        if [ "$(echo $line | cut -f1 -d':' | tr -d ' ')" = "cpucores" ]; then
                cores=`expr $cores + $(echo $line | cut -f2 -d':' | tr -d ' ')`  

        fi
done

ssh $HOST "cat /proc/meminfo" >> tmp5

memfree=$(cat tmp5 | grep MemFree: | cut -f2 -d':' | tr -d ' ')
memtotal=$(cat tmp5 | grep MemTotal: | cut -f2 -d':' | tr -d ' ')

echo "Host: $HOST Cores: $cores TotalMem: $memtotal CurrentFreeMem: $memfree"

#rm flavors

