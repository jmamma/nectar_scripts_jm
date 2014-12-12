import os
import shutil
import yaml
from novaclient.v1_1 import client as nova_client

#DataStructure containing cloud flavours.

#Ascertain these values from NOVA or database at a later date...

flav = [ [4096, 1], [8192, 2], [32768, 8], [65536, 16], [16384, 4] ]
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



def main():
    array = [ 'np-rcc78', 'np-rcc84', 'np-rcc30', 'np-rcc62', 'np-rcc19', 'np-rcc83', 'np-rcc36', 'np-rcc38', 'np-rcc10', 'np-rcc41', 'np-rcc68', 'np-rcc37', 'np-rcc56', 'np-rcc76', 'np-rcc74', 'np-rcc17', 'np-rcc42', 'np-rcc5', 'np-rcc6', 'np-rcc51', 'np-rcc28',$
    array.sort()

    nc = get_nova_client()


    for node in array:
	
    instances_on_host = nc.servers.list(search_opts={'all_tenants': 1, 'host': node})
	
    for instance in instances_on_host:

        f = getattr(instance, 'flavor')
            n = int(str(f['id']))
            NCPU = flav[n][1]
            RAM = flav[n][0]
            STATE = getattr(instance, 'OS-EXT-STS:vm_state')
            NAME = getattr(instance, 'name')
            UID = getattr(instance, 'id')
            CREATED = getattr(instance, 'created')
            IP4 = getattr(instance, 'accessIPv4')
            VOLUME = getattr(instance, 'os-extended-volumes:volumes_attached')
            TENANT_ID = getattr(instance, 'tenant_id')
            USER_ID = getattr(instance, 'user_id')
            IMAGE = getattr(instance, 'image')
            SECURITY = "null"
            #SECURITY = getattr(instance, 'security_groups')
            KEY = getattr(instance, 'key_name')

        #Sanity check
        if int(RAM) > 0:
            node.add_vm(NCPU, RAM, STATE, node.host, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY)





if __name__ == "__main__":
            main()

