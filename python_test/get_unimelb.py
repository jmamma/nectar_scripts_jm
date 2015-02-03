#!/usr/bin/python

import os
import shutil
import yaml
from classes import Instance, Server, Aggregate, Flavor 
from novaclient.v1_1 import client as nova_client
import subprocess
#DataStructure containing cloud flavours.

#Ascertain these values from NOVA or database at a later date...

#flav = [ [4096, 1], [8192, 2], [32768, 8], [65536, 16], [16384, 4] ]
CORES = 24
MEMORY = 131905

def get_nova_client():
    auth_username = os.environ.get('OS_USERNAME', None)
    auth_password = os.environ.get('OS_PASSWORD', None)
    auth_tenant_name = os.environ.get('OS_TENANT_NAME', None)
    auth_url = os.environ.get('OS_AUTH_URL', None)
    auth_vars = (auth_username, auth_password, auth_tenant_name, auth_url)
    for var in auth_vars:
        if not var:
            print "Missing nova environment variables, exiting."
            sys.exit(1)

    nc = nova_client.Client(auth_username,
            auth_password,
            auth_tenant_name,
            auth_url,
            service_type='compute')
    return nc


def cmdline(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

def main():


    array = [ 'qh2-rcc50', 'qh2-rcc54', 'qh2-rcc62', 'qh2-rcc74', 'qh2-rcc75', 'qh2-rcc81', 'qh2-rcc82', 'qh2-rcc38', 'qh2-rcc34', 'qh2-rcc72', 'qh2-rcc59', 'qh2-rcc80', 'qh2-rcc84', 'qh2-rcc13', 'qh2-rcc16', 'qh2-rcc44', 'qh2-rcc58', 'qh2-rcc67', 'qh2-rcc77', 'qh2-rcc65', 'qh2-rcc66', 'qh2-rcc55', 'qh2-rcc9', 'qh2-rcc19', 'qh2-rcc11', 'qh2-rcc33', 'qh2-rcc28', 'qh2-rcc45', 'qh2-rcc15', 'qh2-rcc17', 'qh2-rcc57', 'qh2-rcc47', 'qh2-rcc25', 'qh2-rcc42', 'qh2-rcc8', 'qh2-rcc36', 'qh2-rcc51', 'qh2-rcc52', 'qh2-rcc22', 'qh2-rcc61', 'qh2-rcc64', 'qh2-rcc49', 'qh2-rcc60', 'qh2-rcc24', 'qh2-rcc73', 'qh2-rcc32', 'qh2-rcc40', 'qh2-rcc37', 'qh2-rcc10', 'qh2-rcc29', 'qh2-rcc48', 'qh2-rcc68', 'qh2-rcc69', 'qh2-rcc46', 'qh2-rcc56', 'qh2-rcc63', 'qh2-rcc41', 'qh2-rcc43', 'qh2-rcc31', 'qh2-rcc30', 'qh2-rcc27', 'qh2-rcc23', 'qh2-rcc26', 'qh2-rcc14', 'qh2-rcc18', 'qh2-rcc12', 'qh2-rcc71', 'qh2-rcc79', 'qh2-rcc83', 'qh2-rcc53', 'qh2-rcc35', 'qh2-rcc20', 'qh2-rcc78', 'qh2-rcc21', 'qh2-rcc70', 'qh2-rcc76' ]

    array2 = [ 'np-rcc78', 'np-rcc84', 'np-rcc30', 'np-rcc62', 'np-rcc19', 'np-rcc83', 'np-rcc36', 'np-rcc38', 'np-rcc10', 'np-rcc41', 'np-rcc68', 'np-rcc37', 'np-rcc56', 'np-rcc76', 'np-rcc74', 'np-rcc17', 'np-rcc42', 'np-rcc5', 'np-rcc6', 'np-rcc51', 'np-rcc28', 'np-rcc50', 'np-rcc64', 'np-rcc82', 'np-rcc9', 'np-rcc60', 'np-rcc31', 'np-rcc33', 'np-rcc34', 'np-rcc39', 'np-rcc40', 'np-rcc43', 'np-rcc44', 'np-rcc45', 'np-rcc46', 'np-rcc47', 'np-rcc48', 'np-rcc49', 'np-rcc52', 'np-rcc53', 'np-rcc54', 'np-rcc55', 'np-rcc57', 'np-rcc59', 'np-rcc35', 'np-rcc7', 'np-rcc8', 'np-rcc13', 'np-rcc14', 'np-rcc15', 'np-rcc16', 'np-rcc18', 'np-rcc20', 'np-rcc21', 'np-rcc23', 'np-rcc24', 'np-rcc25', 'np-rcc26', 'np-rcc29', 'np-rcc63', 'np-rcc65', 'np-rcc66', 'np-rcc67', 'np-rcc69', 'np-rcc70', 'np-rcc71', 'np-rcc72', 'np-rcc73', 'np-rcc75', 'np-rcc77', 'np-rcc79', 'np-rcc80', 'np-rcc81', 'np-rcc32', 'np-rcc61', 'np-rcc58', 'np-rcc11', 'np-rcc12' ]
    
    array = array + array2
    array.sort()
    np_aggregate = Aggregate(array, CORES, MEMORY)

    nc = get_nova_client()

    flavors = nc.flavors.list();

    flav = [ ]

    for f in flavors:
        newflav = Flavor(getattr(f,'ram'),getattr(f,'vcpus'),getattr(f,'name'),getattr(f,'id'))
        flav.append(newflav)

    
    
    outputf = open('output.yaml', 'w')



        # print nc.flavors.get(flav).get_keys
#    print nc.hosts.get(np-rcc9')   
#    for host in hosts:


    c = 1
    print "USER_ID - VM_ID - CORES - EMAIL: "

    while c < len(np_aggregate.server_array):
        node = np_aggregate.server_array[c]
        host = node.host
    
        vms_on_host = nc.servers.list(search_opts={'all_tenants': 1, 'host': node.host}) 
    
        d = 1 


        for instance in vms_on_host:
            f = getattr(instance, 'flavor')
            
            for f_search in flav:
                if f_search.id == str(f['id']):
                    flav_match = f_search
            
            NCPU = flav_match.vcpus
            RAM = flav_match.ram         
            n = int(str(f['id']))
            STATE = str(getattr(instance, 'OS-EXT-STS:vm_state'))
            NAME = str(getattr(instance, 'name'))
            UID = str(getattr(instance, 'id'))
            CREATED = str(getattr(instance, 'created'))
            IP4 = getattr(instance, 'accessIPv4')
            VOLUME = str(getattr(instance, 'os-extended-volumes:volumes_attached'))
            TENANT_ID = str(getattr(instance, 'tenant_id'))
            USER_ID = str(getattr(instance, 'user_id'))
            #getattr(getattr(instance, 'image'), 'id')
            temp = getattr(instance, 'image')
            #IMAGE = "null"
          #  IMAGE = str(temp['id']);
            IMAGE = ""
            SECURITY = "null"
            #SECURITY = getattr(instance, 'security_groups')
            KEY = str(getattr(instance, 'key_name'))

            if (NCPU == 8 or NCPU == 16):
                cmd = "keystone user-get " + USER_ID + " | grep email | cut -f3 -d'|' | tr -d ' ' " 
                #"cut -f3 -d':' | tr -d ' ' | tr -d '\|' " 
        
                email = cmdline(cmd) 
                if "unimelb.edu.au" in email: 
                    print USER_ID + " " + UID + " " + str(NCPU) + " " +  email
            #print " UID: " + UID + " USER_ID: " + UID + " CORES: " + str(NCPU) + " EMAIL: " + email

                    #node.add_vm(NCPU, RAM, STATE, node.host, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY)
        c = c + 1
   
        l = 0
     
   

    





if __name__ == "__main__":
            main()

