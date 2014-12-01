#!/usr/bin/python

import os
from novaclient.v1_1 import client as nova_client

flav = [ [4096, 1], [8192, 2], [32768, 8], [65536, 16], [16384, 4] ]

class VM:
    NCPU = 0
    RAM = 0
    STATE = 0
    HOST = 0
    def __init__(self,NCPU,RAM,STATE,HOST):
        self.NCPU = NCPU
        self.RAM = RAM
        self.STATE = STATE
        self.HOST = HOST

class Server:
    processors = 0
    memory = 0
    vm_array = [ VM ]
    def __init__(self, processors, memory):
            self.processors = processors
            self.memory = memory
    
    def add_vm(self,NCPU, RAM, STATE, HOST):
            x = VM(NCPU,RAM,STATE,HOST)
            self.vm_array.append(x)
            
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

def main():


    hosts = [ 'qh2-rcc9' ]

    node = Server(23, 131905)

    print  hosts[0] 

    nc = get_nova_client()

    print nc.flavors.list()
    flavors = nc.flavors.list()

    print flav[0][0] 
            # print nc.flavors.get(flav).get_keys
#    print nc.hosts.get('np-rcc9')   
#    for host in hosts:
    vms_on_host = nc.servers.list(search_opts={'all_tenants': 1, 'host': 'np-rcc9'}) 
    print vms_on_host 

    for instance in vms_on_host:
        print instance.id
        f = getattr(instance, 'flavor')
        n = int(str(f['id']))
        NCPU = flav[n][1]
        RAM = flav[n][0] 
        STATE = getattr(instance, 'OS-EXT-STS:vm_state')
        print "CPUS: ",NCPU,"RAM: ",RAM, "STATE: ", STATE
        node.add_vm(NCPU, RAM, STATE, "np-rcc9")
#   print nc.servers.list('detailed=True')
#print nc.servers.list(a.id)

#    return 0

if __name__ == "__main__":
            main()
