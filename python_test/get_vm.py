#!/usr/bin/python

import os
import shutil
from novaclient.v1_1 import client as nova_client
from jinja2 import Template

flav = [ [4096, 1], [8192, 2], [32768, 8], [65536, 16], [16384, 4] ]

class VM:
    NCPU = 0
    RAM = 0
    STATE = ""
    HOST = ""
    def __init__(self,NCPU,RAM,STATE,HOST):
        self.NCPU = NCPU
        self.RAM = RAM
        self.STATE = STATE
        self.HOST = HOST

class Server:
    processors = 0
    memory = 0
    host = 0
    vm_array = [ VM ]
    def __init__(self,host, processors, memory):
            self.processors = processors
            self.memory = memory
            self.host = host
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

    node = Server(hosts[0], 24, 131905)

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
        if int(RAM) > 0:
            node.add_vm(NCPU, RAM, STATE, "np-rcc9")
#   print nc.servers.list('detailed=True')
#print nc.servers.list(a.id)

    tmpl = Template(u'''\
    <!DOCTYPE html>
    <html>
    <head>
    <title>{{ variable|escape }}</title>
    </head>
    <body>
    <canvas id="myCanvas" width="600" height="500"></canvas>

    <script src="classes.js"></script>
    <script>
    
    var colors = [ 'red', 'yellow', 'green', 'blue', 'pink', 'orange', 'purple', 'skyblue', 'violet' ];
    var offset_x = 25;
    var offset_y = 25;
    var length = 200;
    var blocksize = 20;
    var blockswide = 4; 
    blocksize = (length) * blockswide / {{node.processors}} ;
    

    var server = new Server("{{node.host}}", {{node.processors}}, {{node.memory}}, blockswide);
    
    {%- for vm in vm_array %}
    {% if vm.RAM > 0 %}server.add_vm({{ vm.NCPU }}, {{ vm.RAM }},"{{ vm.STATE }}","{{ vm.HOST }}"){% endif %} 
    {%- endfor %}


    var canvas = document.getElementById('myCanvas');
    var context = canvas.getContext('2d');


    //length = ({{node.processors}} + 0) * blocksize / blockswide;
    
    context.beginPath();
    context.rect(offset_x,offset_y,blockswide * blocksize, length);
    context.stroke();

    for (y = 0; y < {{node.processors}} / blockswide; y++) {
        for (x = 0; x < blockswide; x++) {
            context.beginPath();
            context.rect(offset_x + x * blocksize,offset_y + y * blocksize, blocksize, blocksize);
            context.stroke();
        }
    }

    os = offset_x + blockswide * blocksize + offset_x;

    context.beginPath();
    context.rect(os,offset_y,blockswide * blocksize, length);
    context.fillStyle = "lime";
    context.fill();    
    context.stroke();

    sofar=length;
    coresleft = server.processors;
    for (i = 0; i < server.vm_array.length; i++) {
        cores = server.vm_array[i].NCPUs;
        a = 0 + coresleft % 4;
        for (n = cores; n > 0; n--) {
                context.beginPath();
                context.rect(os + a,offset_y + (server.processors / coresleft) * blocksize, blocksize ,blocksize);
        
                context.fillStyle = colors[i];
                context.fill();
                context.stroke();
                a = a + 1;
                if (a > 4) {
                a = 0;  
                }

        }
        coresleft = coresleft - server.vm_array[i].NCPUs;

        proportion = ((server.vm_array[i].RAM / server.memory) * length);
    
        context.beginPath();
            context.rect(os,offset_y + sofar,blockswide * blocksize, proportion * -1);
        context.fillStyle = colors[i];
        context.fill();
        context.stroke();
        sofar = sofar - proportion;
    
    }

    </script>
    {% for x in range(1,node.processors) %}
        {{ x }}
    
    {% endfor %}
    
    {%- for vm in vm_array %}
        {{ vm.NCPU }}{% if not loop.last %},{% endif %}
    {%- endfor %}
    
    </body>
    </html>
    ''')
   

    template_output = tmpl.render(                    
    node = node,
    variable = "Title of page",
    vm_array = node.vm_array
    )

    print template_output

    with open('output.html','w') as f:
            f.write(template_output)

    shutil.copyfile('output.html','/var/www/html/output.html')
    shutil.copyfile('classes.js','/var/www/html/classes.js')
#    return 0

if __name__ == "__main__":
            main()
