#!/usr/bin/python

import os
import shutil
import yaml
import ast
from classes import Instance, Server, Aggregate

from novaclient.v1_1 import client as nova_client
from jinja2 import Environment, FileSystemLoader, Template

flav = [ [4096, 1], [8192, 2], [32768, 8], [65536, 16], [16384, 4] ]

print os.getcwd()
print os.path.join(os.path.dirname(__file__), 'templates')

#env = Environment(loader=FileSystemLoader("templates"),autoescape=True)
env = Environment(loader=FileSystemLoader("templates"),autoescape=True)


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

CORES = 24
MEMORY = 131905

def main():
    array = [ 'np-rcc78', 'np-rcc84', 'np-rcc30', 'np-rcc62', 'np-rcc19', 'np-rcc83', 'np-rcc36', 'np-rcc38', 'np-rcc10', 'np-rcc41', 'np-rcc68', 'np-rcc37', 'np-rcc56', 'np-rcc76', 'np-rcc74', 'np-rcc17', 'np-rcc42', 'np-rcc5', 'np-rcc6', 'np-rcc51', 'np-rcc28',     'np-rcc50', 'np-rcc64', 'np-rcc82', 'np-rcc9', 'np-rcc60', 'np-rcc31', 'np-rcc33', 'np-rcc34', 'np-rcc39', 'np-rcc40', 'np-rcc43', 'np-rcc44', 'np-rcc45', 'np-rcc46', 'np-rcc47', 'np-rcc48', 'np-rcc49', 'np-rcc52', 'np-rcc53', 'np-rcc54', 'np-rcc55', 'np-rcc57', 'np-rcc59', 'np-    rcc35', 'np-rcc7', 'np-rcc8', 'np-rcc13', 'np-rcc14', 'np-rcc15', 'np-rcc16', 'np-rcc18', 'np-rcc20', 'np-rcc21', 'np-rcc23', 'np-rcc24', 'np-rcc25', 'np-rcc26', 'np-rcc27', 'np-rcc29', 'np-rcc63', 'np-rcc65', 'np-rcc66', 'np-rcc67', 'np-rcc69', 'np-rcc70', 'np-rcc71', 'np-rcc72'    , 'np-rcc73', 'np-rcc75', 'np-rcc77', 'np-rcc79', 'np-rcc80', 'np-rcc81', 'np-rcc32', 'np-rcc61', 'np-rcc58' ]
    #array = [ 'np-rcc60', 'np-rcc31', 'np-rcc33', 'np-rcc34', 'np-rcc39', 'np-rcc40', 'np-rcc43', 'np-rcc44', 'np-rcc45', 'np-rcc46', 'np-rcc47', 'np-rcc48', 'np-rcc49', 'np-rcc52', 'np-rcc53', 'np-rcc54', 'np-rcc55', 'np-rcc57', 'np-rcc59', 'np-    rcc35', 'np-rcc7', 'np-rcc8', 'np-rcc13', 'np-rcc14', 'np-rcc15', 'np-rcc16', 'np-rcc18', 'np-rcc20', 'np-rcc21', 'np-rcc23', 'np-rcc24', 'np-rcc25', 'np-rcc26', 'np-rcc27', 'np-rcc29', 'np-rcc63', 'np-rcc65', 'np-rcc66', 'np-rcc67', 'np-rcc69', 'np-rcc70', 'np-rcc71', 'np-rcc72'    , 'np-rcc73', 'np-rcc75', 'np-rcc77', 'np-rcc79', 'np-rcc80', 'np-rcc81', 'np-rcc32', 'np-rcc61', 'np-rcc58' ]

    array.sort()
    np_aggregate = Aggregate(array, CORES, MEMORY)


    nc = get_nova_client()

    print nc.flavors.list()
    flavors = nc.flavors.list()

    print flav[0][0] 
            # print nc.flavors.get(flav).get_keys
#    print nc.hosts.get(np-rcc9')   
#    for host in hosts:

    print np_aggregate.server_array
    
    c = 1
    print "okay" 
    print len(np_aggregate.server_array)          

    while c < len(np_aggregate.server_array):
        node = np_aggregate.server_array[c]
        host = node.host
        
        print node.host
        vms_on_host = nc.servers.list(search_opts={'all_tenants': 1, 'host': node.host}) 
        
        d = 1 
        for instance in vms_on_host:
            f = getattr(instance, 'flavor')
            n = int(str(f['id']))
            NCPU = flav[n][1]
            RAM = flav[n][0] 
            STATE = str(getattr(instance, 'OS-EXT-STS:vm_state'))
            NAME = str(getattr(instance, 'name'))
            UID = str(getattr(instance, 'id'))
            CREATED = str(getattr(instance, 'created'))
            IP4 = getattr(instance, 'accessIPv4')
            VOLUME = str(getattr(instance, 'os-extended-volumes:volumes_attached'))
            TENANT_ID = str(getattr(instance, 'tenant_id'))
            USER_ID = str(getattr(instance, 'user_id'))
            print vms_on_host
            print type(getattr(instance, 'image'))
            #getattr(getattr(instance, 'image'), 'id')
            temp = getattr(instance, 'image')
            #IMAGE = "null"
            IMAGE = str(temp['id']);
            SECURITY = "null"
            #SECURITY = getattr(instance, 'security_groups')
            KEY = str(getattr(instance, 'key_name'))


            print STATE
            if int(RAM) > 0:
                node.add_vm(NCPU, RAM, STATE, node.host, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY)
        c = c + 1
       
        l = 0
        
        while l < len(node.vm_array):
            print node.vm_array[l]
            print yaml.dump(node.vm_array[l])
            l = l + 1
        print len(node.vm_array)
        print len(np_aggregate.server_array[1].vm_array)          
        print len(np_aggregate.server_array[16].vm_array)          

#   print nc.servers.list('detailed=True')
#print nc.servers.list(a.id)

    tmpl_header = env.get_template('template_header.html') 
    
    tmpl_body = env.get_template('template_body.html');
   
    tmpl_footer = env.get_template('template_footer.html');

    template_output = tmpl_header.render(
    np_aggregate = np_aggregate,
    node = node,
    variable = "Title of page",
    vm_array = node.vm_array
                    
    )
    template_output2 = tmpl_body.render(                    
    np_aggregate = np_aggregate,
    node = node,
    variable = "Visual Cloud",
    vm_array = node.vm_array
    )
    template_output3 = tmpl_footer.render(node = node, vm_array = node.vm_array)


    print template_output

    with open('output.html','w') as f:
        f.write(template_output)
        f.write(template_output2)
        f.write(template_output3)


    shutil.copyfile('output.html','/var/www/html/output.html')
    shutil.copyfile('classes.js','/var/www/html/classes.js')
#    return 0

if __name__ == "__main__":
            main()
