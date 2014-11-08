
#!/bin/bash

#Run cleanup, if script is terminated early.

trap "cleanUp 2" SIGHUP SIGINT SIGTERM  

spinner="-/|\\"


id=$1

mount_dir_0="/mnt/vdd/compromised_vms/$id"
mount_dir_1="$mount_dir_0/root"
mount_dir_2="$mount_dir_0/ephemeral"

tunnel=suse

source helper.sh

cd $mount_dir_0


getdisks() {

    ssh_tunnel $tunnel $node $2 $3 
    if [ "$?" -gt "0" ]; then
        cleanUp 5 "SSH Tunnel Failed"
        return 1
    fi 

    rsync -e "ssh -p $3" -vz $2@localhost:~/test .
    echo -e "\n${Green}Stage 0: Get disk data from VM $id${NoColor}\n"
    
    if [ ! -e $mount_dir_0/disk ]; then
        echo "${Orange}File does not exist.. ssh $mount_dir_0/disk${NoColor}"
    fi

    if [ ! -e $mount_dir_0/disk.local ]; then
        echo "${Orange}file does not exist.. ssh $mount_dir_0/disk.local${NoColor}"
    fi


}

mountdisks() {

    echo -e "\n${Green}Stage 1: Mount Disks${NoColor}\n"

    #Create the Mount Directories

    echo -e "Creating Mount Directory: $mount_dir_1"
    sudo mkdir -p $mount_dir_1 
    echo -e "Creating Mount Directory: $mount_dir_2\n"
    sudo mkdir -p $mount_dir_2

    #Load the Kernal Module

    if [ `lsmod | grep nbd | wc -l` -gt 0 ]; then

        echo "Qemu Kernal Module already loaded"
        else
        sudo modprobe nbd max_part=63   
        echo "Qemu Kernal Module loaded"
        
    fi

    #Use qemu-nbd to load the first disk image to a device
    
    echo -e "\nDisk 1, root, disk:"
    
    if $(sudo qemu-nbd -c /dev/nbd0 disk; wait); then
        echo "/dev/nbd0 created"
    else 
        cleanUp 1 "qemu1 failed"
    fi


    #Add process of previous command to our Process Array (For termination Later)
    addProcess $(ps ax | grep "qemu-nbd -c /dev/nbd0 disk" | head -1 | cut -f1 -d' ')
 
    if $(sudo mount /dev/nbd0p1 $mount_dir_1); then
        echo -e "Mount Successful: $mount_dir_1\n"
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
       echo -e "Mount Successful: $mount_dir_2\n"
   else
       cleanUp 1 "mount2 failed"
   fi
    
    df -h
    
    #ps waux | grep ${process[0]}
}


create_tar() {
    
    #Remove the old log file (if it exists)
    rm $1.log
    #Remove the leading slash from the path
    path_tmp=$(echo $2 | cut -c2-)

    echo -e "\nCounting Files... "
    #Count number of files in mount directory.

    num_files=$(sudo find $2 | wc -l)
    echo -ne "$num_files\n"

    #Create an archive of the mounted directory by running tar in the background

    (sudo tar -vzcf $1 -C / $path_tmp > $1.log) & pid_tmp1=$!

    #Whilst the tar process is still runnning display progress:

    while [ $(ps -p $pid_tmp1 | wc -l) -gt 1 ] ; do

    #Check progress every 100ms.
        sleep 0.1
    #Count number of files processed so far.
        so_far=$(cat $1.log | wc -l) 
    #Rotate spinner glyph
        spinner=$(echo -n $spinner | tail -c 1)$(echo -n $spinner | head -c 3)                    
      
    #Draw progress bar
        echo -ne "\r $(progressbar $so_far $num_files) $(echo -n $spinner | head -c 1) "
        echo -n "Files: $num_files/$so_far - SizeOf $1: $(du -h $1 | cut -f1 -d$'\t') "      

    done

}

tardisks() {

    files=($mount_dir_1/*)
    files2=($mount_dir_2/*)
    
    cd $mount_dir_0

    echo -e "\n${Green}Stage 3: Create Compressed Archives (TAR) ${NoColor}"

    if [ ${#files[@]} -gt 0 ]; then


        echo -e "Creating Archive - root.tar.gz"
    
        echo -e "\n Files were detected in $mount_dir_1"

        if [ ! -e root.tar.gz ]; then 

        create_tar root.tar.gz $mount_dir_1


        else
            echo $mount_dir_0"/root.tar.gz already exists, skipping"
        fi
    fi

    if [ ${#files2[@]} -gt 0 ]; then
        echo -e "\nCreating Archive ephemeral.tar.gz"
        echo -e "\n Files were detected in $mount_dir_2"
       
        if [ ! -e ephemeral.tar.gz ]; then 
        
                create_tar ephemeral.tar.gz $mount_dir_2
         
        else
            echo $mount_dir_0"/ephemeral.tar.gz already exists, skipping"
        fi   
       

    fi

}


cleanUp() {
    
    if [ $1 == 0 ]; then
        echo -e "\n${Green}Success: Exiting"
    fi
    if [ $1 == 2 ]; then
        echo -e "\n${Red}User termination."
    else
        echo -e "\n${Red}Error: " $2
    fi
    
    if grep -qs $mount_dir_1 /proc/mounts; then
        sudo umount $mount_dir_1
    fi

    if grep -qs $mount_dir_2 /proc/mounts; then
        sudo umount $mount_dir_2
    fi
    
    killProcess
    exit 1
}

#Script Start:

if [ -z $id ]; then
    echo "${Red}Error: Must specify VM ID as argument"
    exit 1
fi 

node=$(getNode $id) 
node=128.250.164.237

if [ "$node" = "1" ] || [ -z $node ] ; then
        cleanUp 1 "Could not find Node"
fi

echo -e "\n\n"
echo -e "${Green}--------------------------"
echo -e "VM Data Backup"
echo -e "--------------------------\n"
echo -e "${NoColor}VM: $id \nHosted on: $node\n"

#If local files do not exist... rsync files from node

getdisks $node j 5555
mountdisks
tardisks
sleep 1
cleanUp 0 
