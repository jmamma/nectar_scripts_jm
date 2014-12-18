#!/usr/bin/python

import os
import shutil
import yaml
import jsonpickle    
import subprocess
import private

from classes import Instance, Server, Aggregate 
from novaclient.v1_1 import client as nova_client

#DataStructure containing cloud flavours.

#Ascertain these values from NOVA or database at a later date...

flav = [ [4096, 1], [8192, 2], [32768, 8], [65536, 16], [16384, 4] ]
CORES = 24
MEMORY = 131905

def cmdline(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return out

def get_nova_client():
    cmdstr = '. ' + openrc-admin
    cmdline(openrc-admin)
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

outputf = open('output.yaml', 'w')

nc = get_nova_client()

flavors = nc.flavors.list()

aggregate_list = nc.aggregates.list();

aggregates = [ ]

for aggregate in aggregate_list:
    aggregates.append(aggregate.id)

print "Content-type: application/json"
print
print jsonpickle.encode(aggregates, unpicklable=False)



