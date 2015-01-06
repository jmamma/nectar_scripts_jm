#!/usr/bin/python

import os
import shutil
import yaml
import cgi
from private import *
import jsonpickle    
from classes import Instance, Server, Aggregate
from novaclient.v1_1 import client as nova_client
from classes import Instance, Server, Aggregate, Flavor 

#flav = [ [4096, 1], [8192, 2], [32768, 8], [65536, 16], [16384, 4] ]

CORES = 24
MEMORY = 128812 - 30507

def get_nova_client():
    with open(openrc_admin,'r') as f:
        for line in f:
            firstword = line.split(' ')[0] 
            if firstword == "export":
                line = line.replace("\n",'').replace('"','')
                var_n = line.split(' ')[1].split('=')[0]
                if var_n == "OS_USERNAME":
                    auth_username = line.split('=')[1]
                if var_n == "OS_PASSWORD":
                    auth_password = line.split('=')[1]
                if var_n == 'OS_TENANT_NAME':
                    auth_tenant_name = line.split('=')[1]
                if var_n == 'OS_AUTH_URL':
                    auth_url = line.split('=')[1]


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


#stream = file('/var/www/html/output.yaml', 'r')


nc = get_nova_client()

#aggregate = cgi.getfirst('aggregate')
aggregate_list = nc.aggregates.list();

aggregates = [ ]

flavors = nc.flavors.list();

flav = [ ]

for f in flavors:
    newflav = Flavor(getattr(f,'ram'),getattr(f,'vcpus'),getattr(f,'name'),getattr(f,'id'))
    flav.append(newflav)

print "Content-type: application/json"
print

form = cgi.FieldStorage()
aggregate = form.getvalue('aggregate')


if not aggregate: 
    aggregate = "nectar!melbourne!qh2@netapp"


for aggregate_c in aggregate_list:
        #    print aggregate_c.name 
#    print nc.aggregates.get_details(aggregate_c)
    if aggregate == aggregate_c.name:
        hosts = getattr(nc.aggregates.get_details(aggregate_c),'hosts')


aggreg_obj = Aggregate(hosts, CORES, MEMORY) 

#  print np_aggregatr!melbourne!qh2@4array

c = 1

while c < len(aggreg_obj.server_array):
    node = aggreg_obj.server_array[c]
    host = node.host

    host_name_full = aggregate.split('@')[0] + "@" + node.host

#Used total
    
    host_details = nc.hosts.get(host_name_full)
    host_details_1 = vars(host_details[1]) 
    host_details_0 = vars(host_details[0])
    host_details_4 = vars(host_details[4])
    host_details_3 = vars(host_details[3])
    host_details_2 = vars(host_details[2])

    memory_os_reserved = host_details_1['memory_mb'] - host_details_2['memory_mb']  

#    print host_details_0
#    print host_details_1
#    print host_details_2
#    print host_details_3
#    print host_details_4

    node.processors = host_details_0['cpu']
    node.memory = host_details_0['memory_mb'] - memory_os_reserved
    vms_on_host = nc.servers.list(search_opts={'all_tenants': 1, 'host': node.host}) 

    d = 1 

    for instance in vms_on_host:
        f = getattr(instance, 'flavor')
        for f_search in flav:
            if f_search.id == str(f['id']):
                flav_match = f_search
        
        NCPU = flav_match.vcpus
        RAM = flav_match.ram 
        STATE = str(getattr(instance, 'OS-EXT-STS:vm_state'))
        NAME = str(getattr(instance, 'name'))
        UID = str(getattr(instance, 'id'))
        INSTANCE_NAME = str(getattr(instance, 'OS-EXT-SRV-ATTR:instance_name'))
        CREATED = str(getattr(instance, 'created'))
    
        IP4 = str(getattr(instance, 'accessIPv4'))

        volstr = ""
        for vol in getattr(instance, 'os-extended-volumes:volumes_attached'):
            volstr = volstr + " " +  str(vol['id'])
        VOLUME = volstr
        
        TENANT_ID = str(getattr(instance, 'tenant_id'))
        USER_ID = str(getattr(instance, 'user_id'))
        img = getattr(instance, 'image')
        if img: 
            IMAGE = str(img['id'])
        SECURITY = "null"
        #SECURITY = getattr(instance, 'security_groups')
        KEY = str(getattr(instance, 'key_name'))

        
        if int(RAM) > 0:
            node.add_vm(NCPU, RAM, STATE, node.host, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY, INSTANCE_NAME)
    c = c + 1

    l = 0


 #   print jsonpickle.encode(np_aggregate, unpicklable=False)

print jsonpickle.encode(aggreg_obj, unpicklable=False)

#self.response.headers['Content-Type'] = "application/json"
#self.response.out.write(jsonpickle.encode(np_aggregate, unpicklable=False)

#print
#print "<html><head>"
#print ""
#rint "</head><body>"
#print "Content-type: application/json"
#print "</body></html>"

#    return 0

