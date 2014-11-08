#!/bin/bash

#Justin Mammarella 06/11/2014

#Helper functions called in by other scripts.

# Reset
NoColor='\e[0m'       # Text Reset

# Regular Colors
Black='\e[0;30m'        # Black
Red='\e[0;31m'          # Red
Green='\e[0;32m'        # Green
Yellow='\e[0;33m'       # Yellow
Blue='\e[0;34m'         # Blue
Purple='\e[0;35m'       # Purple
Cyan='\e[0;36m'         # Cyan
White='\e[0;37m'        # White

calc() {
        echo awk \'BEGIN { print "$@" }\' | /bin/bash 
}

get_integer() {
   echo $(echo "$1" | cut -f1 -d'.')
}

#Draw a Progress Bar on screen
#progressbar <a> <b>
#where a is number of items so far.
#b is total items
progressbar() {


 
    #Cut out any decimal places to allow interger comparison

    arg1=$(get_integer "$1")
    arg2=$(get_integer "$2")
   
    if [ $arg1 -gt $arg2 ]; then
            arg1=$2
    else
            arg1=$1
    fi

    clc=$(calc "$arg1 / $arg2 * 100")
    clc=$(get_integer $clc)
                    
    clc2=$(calc "$clc / 2") 
    clc2=$(get_integer $clc2)
                                
    bar=""
    a=0

    while [ $a -lt $clc2 ]; do
        bar=$bar'='
        a=`expr $a + 1`
    done
    
    a=0
    
    while [ $a -lt $(expr 50 - $clc2) ]; do
        bar=$bar'-'
        a=`expr $a + 1`    
    done


    echo -n "$clc% [ $bar ] " 

}

check_admin_credentials() {
    
        
    if [ "$OS_USERNAME" = "admin-melbourne" ] && [ "$OS_TENANT_ID" = "2" ]; then
            echo "Admin Credentials Supplied"
            return 0
        else
            echo "Admin Credentials Not supplied"        
            return 1
    fi;


}

get_volumes() {
        if [ -z check_admin_credentials ]; then
            return 1
        fi

        if [ -z $1 ]; then
            echo "No VM ID supplied"    
            return 1
        else
            nova show $1 |  grep "OS-EXT-SRV-ATTR:hypervisor_hostname" | cut -f3 -d'|' | tr -d ' ' 
                
        fi

}

getNode() {

        if [ -z check_admin_credentials ]; then
            return 1
        fi
        
        if [ -z $1 ]; then
            echo "No VM ID supplied"    
            return 1
        else
            nova show $1 |  grep "OS-EXT-SRV-ATTR:hypervisor_hostname" | cut -f3 -d'|' | tr -d ' ' 
                
        fi

}

