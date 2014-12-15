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

        
    stream = file('output.yaml', 'r')
    np_aggregate = yaml.load(stream)
    print np_aggregate     
  #  print np_aggregate.server_array

    tmpl_header = env.get_template('template_header.html') 
    
    tmpl_body = env.get_template('template_body.html')
   
    tmpl_footer = env.get_template('template_footer.html')

    template_output = tmpl_header.render(
    np_aggregate = np_aggregate,
    variable = "Visual Cloud",
    processors = CORES                 
    )
    template_output2 = tmpl_body.render(                    
    np_aggregate = np_aggregate,
    variable = "Visual Cloud",
    processors = CORES                 

    )
    template_output3 = tmpl_footer.render()


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
