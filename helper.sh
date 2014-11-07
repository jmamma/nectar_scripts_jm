#!/bin/bash

#Justin Mammarella 06/11/2014

#Helper functions called in by other scripts.

check_admin_credentials() {
    
        
    if [ "$OS_USERNAME" = "admin-melbourne" ] && [ "$OS_TENANT_ID" = "2" ]; then
            echo "Admin Credentials Supplied"
            return 0
        else
            echo "Admin Credentials Not supplied"        
            return 1
    fi;


}

getNode() {

        if [ ! check_admin_credentials ]; then
            return 1
        fi
        
        if [ -z $1 ]; then
            echo "No VM ID supplied"    
            return 1
        else
            nova show $1 |  grep "OS-EXT-SRV-ATTR:hypervisor_hostname" | cut -f3 -d'|' | tr -d ' ' 
                
        fi

}
