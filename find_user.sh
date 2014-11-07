#!/bin/sh

if [ "$OS_USERNAME" = "admin-melbourne" ] && [ "$OS_TENANT_ID" = "2" ]; then

    echo "Admin Credentials Supplied"
else
    echo "Admin Credentials Not supplied"        
    exit
fi;
if [ ! -z $1 ]; then
    echo -e "\nSearching Keystone for: $1\n"
    keystone user-list | grep $1  > tmpsearch
    
    count=`cat tmpsearch | wc -l`
    
    if [ $count -gt 1 ]; then
            echo -e "\nFound $count users"
            echo "==================================================" 
            echo "Select the appropriate user from list"
            echo "=================================================="
            echo "0: None (Exit)"
            n=0
         
            until [ $n -eq $count ]
            do
                n=`expr $n + 1` 
                
                line=$(sed -n $n'p' tmpsearch | cut -f3 -d'|' | tr -d ' ' )
                echo "$n: $line" 
            done
            echo "==================================================" 
                      
            read -e -p "Enter a number corresponding to the user above: " SELECT
    fi
    echo "select" $SELECT $count
    if [ $SELECT -eq 0 ] || [ $SELECT -gt $count ]; then
            echo "Exiting"
            exit  
    else
            USER=$(sed -n $SELECT'p' tmpsearch | cut -f3 -d'|')
            USERID=$(sed -n $SELECT'p' tmpsearch | cut -f2 -d'|')
    fi;


    echo "==================================================" 
    echo $USER $USERID
    echo "=================================================="
    


fi;

if [ -e tmpsearch ]; then
        rm tmpsearch
fi;
