#!/bin/bash

#Initialise Process Array

process[0]=-1
processcount=0
id=$1

mount_dir_1="/mnt/compromised_vms/$id/root"
mount_dir_2="/mnt/compromised_vms/$id/ephemeral"

source helper.sh

mountdisks() {

    echo "Get data from Compromised VM"
   
    echo "Mount Disks"

    #Create the Mount Directories
    sudo mkdir -p $mount_dir_1 
    sudo mkdir -p $mount_dir_2

    #Load the Kernal Module

    if [ `lsmod | grep nbd | wc -l` -gt 0 ]; then

        echo "Qemu Kernal Module Loaded"
        else
        sudo modprobe nbd max_part=63   

    fi

    #Use qemu-nbd to load the first disk image to a device

    echo "Disk 1"
    
    if $(sudo qemu-nbd -c /dev/nbd0 disk; wait); then
        echo "Blah"
    else 
        cleanUp 1 "qemu failed"
    fi


    #Add process of previous command to our Process Array (For termination Later)
    addProcess $(ps ax | grep "qemu-nbd -c /dev/nbd0 disk" | head -1 | cut -f1 -d' ')

     
    if $(sudo mount /dev/nbd0p1 $mount_dir_1); then
        echo "Mount Successful: $mount_dir_1"
    else
        cleanUp 1 "mount1 failed"
    fi
            
    


    #ps waux | grep ${process[0]}
}


addProcess() {

    #process+=$1
    process[$processcount]=$1

    echo "Added Process" ${process[$processcount]}
    processcount=`expr $processcount + 1`

}

cleanUp() {
    
    if [ $1 = 0 ]; then
    echo "Success: Exiting"
    else
    echo "Something went wrong: " $2
    fi
    
    for i in "${process[@]}"
    do
            if [ $i != -1 ]; then
                echo "Killing PID: " $i 
                sudo kill -9 $i
            fi
    done
    exit 1
}

#Script Start:

node=$(getNode $id) 

if [ "$node"="1" ]; then
        cleanUp 1 "Could not find Node"
fi
echo "VM: " $id "Hosted on: " $node


mountdisks
sleep 1
cleanUp 0 
