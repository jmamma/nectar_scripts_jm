#!/bin/bash

#Initialise Process Array

process[0]=-1
processcount=0
id=$1

mount_dir_0="/mnt/vdd/compromised_vms/$id"
mount_dir_1="$mount_dir_0/root"
mount_dir_2="$mount_dir_0/ephemeral"

source helper.sh

cd $mount_dir_0


getdisks() {
    
    echo "Get disk data from VM: " $id
    
    if [ ! -e $mount_dir_0/disk ]; then
        echo "file does not exist.. ssh" $mount_dir_0/disk
    fi

    if [ ! -e $mount_dir_0/disk.local ]; then
        echo "file does not exist.. ssh" $mount_dir_0/disk.local
    fi


}

mountdisks() {

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
    
    echo "Disk 1, root, disk"
    
    if $(sudo qemu-nbd -c /dev/nbd0 disk; wait); then
        echo "/dev/nbd0 created"
    else 
        cleanUp 1 "qemu1 failed"
    fi


    #Add process of previous command to our Process Array (For termination Later)
    addProcess $(ps ax | grep "qemu-nbd -c /dev/nbd0 disk" | head -1 | cut -f1 -d' ')
 
    if $(sudo mount /dev/nbd0p1 $mount_dir_1); then
        echo "Mount Successful: $mount_dir_1"
    else
        cleanUp 1 "mount1 failed"
    fi
            
    echo "Disk 2, ephemeral,disk.local"
    if $(sudo qemu-nbd -c /dev/nbd1 disk.local; wait); then
            
        echo "/dev/nbd1"
    else 
        cleanUp 1 "qemu2 failed"
    fi

    #Add process of previous command to our Process Array (For termination Later)
    addProcess $(ps ax | grep "qemu-nbd -c /dev/nbd1 disk.local" | head -1 | cut -f1 -d' ')


   if $(sudo mount /dev/nbd1 $mount_dir_2); then
       echo "Mount Successful: $mount_dir_2"
   else
       cleanUp 1 "mount2 failed"
   fi
    
    echo -e "\n"
    df -h
    echo -e "\n"
    
    #ps waux | grep ${process[0]}
}

tardisks() {

    files=($mount_dir_1/*)
    files2=($mount_dir_2/*)
    
    cd $mount_dir_0

    echo "Tar"

    if [ ${#files[@]} -gt 0 ]; then

        echo -e "\n Files were detected in $mount_dir_1"
        echo -e "Creating Archive root.tar.gz"

        if [ ! -e root.tar.gz ]; then 
                rm tar1.log

                echo "Counting Files:"
                num_files=$(sudo find $mount_dir_1 -type f | wc -l)
               # echo $num_files
                (sudo tar -vzcf root.tar.gz $mount_dir_1 > tar1.log) &
                pid_tmp1=$!
               # echo $pid_tmp1
                
                while [ $(ps -p $pid_tmp1 | wc -l) -gt 1 ] ; do
                    sleep 1
                    so_far=$(wc -l < tar1.log) 
                    #echo $num_files
                    #echo $so_far
                    #calc=$(div $so_far $num_file)
                    #echo $calc
                    
                    clc= $(calc "$so_far / $num_files * 100")
                    echo -ne "\r $clc% $num_files $so_far"
                done

          echo "hmm" 
                sudo kill -9 $1 

        else
            echo $mount_dir_0"/root.tar.gz already exists"
        fi
    fi

    if [ ${#files2[@]} -gt 0 ]; then
        echo -e "\n Files were detected in $mount_dir_2"
        echo -e "Creating Archive ephemeral.tar.gz"
       
       
        if [ ! -e root.tar.gz ]; then 
                rm tar2.log
        
                sudo tar -vzcf ephemeral.tar.gz $mount_dir_2 > tar2.log   

        else
            echo $mount_dir_0"/ephemeral.tar.gz already exists"
        fi   
       

    fi

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
    
    if grep -qs $mount_dir_1 /proc/mounts; then
        sudo umount $mount_dir_1
    fi

    if grep -qs $mount_dir_2 /proc/mounts; then
        sudo umount $mount_dir_2
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

if [ -z $id ]; then
    echo "Error: Must specify VM ID as argument"
    exit 1
fi 

node=$(getNode $id) 

if [ "$node" = "1" ] || [ -z $node ] ; then
        cleanUp 1 "Could not find Node"
fi

echo "VM: " $id "Hosted on: " $node

#If local files do not exist... rsync files from node
getdisks
mountdisks
tardisks
sleep 1
cleanUp 0 
