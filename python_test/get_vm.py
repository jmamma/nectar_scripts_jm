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
    def __init__(self,host, processors, memory):
            
            self.vm_array = [ ]
    
            self.processors = processors
            self.memory = memory
            self.host = host
    def add_vm(self,NCPU, RAM, STATE, HOST):
            x = VM(NCPU,RAM,STATE,HOST)
            self.vm_array.append(x)

class Aggregate:
    def __init__(self, hostlist, processors, memory):
        self.server_array = [ ]
        for host in hostlist:
            x = Server(host,processors,memory)
            self.server_array.append(x)


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
            STATE = getattr(instance, 'OS-EXT-STS:vm_state')
            print STATE
            if int(RAM) > 0:
                node.add_vm(NCPU, RAM, STATE, node.host)
        c = c + 1
       
        l = 0
        
        while l < len(node.vm_array):
            print node.vm_array[l]
            l = l + 1
        print len(node.vm_array)
        print len(np_aggregate.server_array[1].vm_array)          
        print len(np_aggregate.server_array[16].vm_array)          

#   print nc.servers.list('detailed=True')
#print nc.servers.list(a.id)

    tmpl_header = Template(u'''\
        <!DOCTYPE html>
        <html>
        <head>
        <title>{{ variable|escape }}</title>
        </head>
        <body>
        <canvas id="myCanvas" width="1200" height="10000"></canvas>

        <script src="classes.js"></script>
        <script>
    
        var colors = [ 'red', 'yellow', 'green', 'blue', 'pink', 'orange', 'purple', 'skyblue', 'violet', 'chocolate', 'firebrick', 'indigo', 'indianred', 'khaki', 'navy', 'olive', 'tan', 'coral', 'cornsilk', 'crimson', 'darkcyan', 'moccasin'];
        var offset_x = 25;
        var offset_y = 25;
        var length = 200;
        var blocksize = 20;
        var blockswide = 4; 
        var overextend = 32;
        blocksize = (length) * blockswide / ({{node.processors}} + overextend) ;
	''')

    tmpl_body = Template(u'''\
        
        var np_aggregate = new Aggregate();

        {% for node_x in np_aggregate.server_array %}
        current_server = np_aggregate.add_server("{{node_x.host}}", {{node_x.processors}}, {{node_x.memory}}, blockswide);
    
        {%- for vm in node_x.vm_array %}
        {% if vm.RAM > 0 %}current_server.add_vm({{ vm.NCPU }}, {{ vm.RAM }},"{{ vm.STATE }}","{{ vm.HOST }}");{% endif %} 
        {%- endfor %}

        {%- endfor %}
        
        var d_board = new DrawingBoard();
        
        context = d_board.context;
        d_board.add_layer();
        d_board.add_layer();
        countx = 0;
        county = 0;

        key = 0

        for (key = 0; key < np_aggregate.server_array.length; key++) {

            shift_x = (blockswide * blocksize * 2 + offset_x * 2) * countx; 
            shift_y = (length + offset_y * 2) * county;

            //length = ({{node.processors}} + 0) * blocksize / blockswide;
   
            d_board.add_drawobj("text", np_aggregate.server_array[key].name, offset_x + shift_x, offset_y / 2 + shift_y, 0, 0, "black", np_aggregate.server_array[key],0);

            d_board.add_drawobj("rect", "", offset_x + shift_x,offset_y + shift_y + length,blockswide * blocksize, -1 * blocksize * {{node.processors}} / blockswide, "lime", np_aggregate.server_array[key],0);
            context.stroke();

            for (y = 0; y < ({{node.processors}} + overextend) / blockswide; y++) {
                for (x = 0; x < blockswide; x++) {

        //    d_board.add_drawobj("rect","",shift_x + offset_x + x * blocksize,shift_y + offset_y + y * blocksize, blocksize, blocksize, "null", np_aggregate.server_array[key],0);
                }
            }

            os = offset_x + blockswide * blocksize + offset_x;

            d_board.add_drawobj("rect","", os + shift_x,offset_y + shift_y,blockswide * blocksize, length, "lime", np_aggregate.server_array[key],0);

            sofar=length;
            coresleft = np_aggregate.server_array[key].processors;
    
            x = 0
            y = 0

            //Iterate through each node/server to

            for (i = 0; i < np_aggregate.server_array[key].vm_array.length; i++) {
                            

                    cores = np_aggregate.server_array[key].vm_array[i].NCPU;
    
                    for (n = cores; n > 0; n--) {
            d_board.add_drawobj("rect","", shift_x + offset_x + (x * blocksize),shift_y + offset_y + length - (blocksize * (y + 1)), blocksize ,blocksize, colors[i], np_aggregate.server_array[key].vm_array[i],0);
 
                        x = x + 1;
                    
                        if (x >= blockswide) {
                         x = 0;  
                         y = y + 1;
                        }

                 }

             if (np_aggregate.server_array[key].vm_array[i].STATE != "suspended") {  

                coresleft = coresleft - np_aggregate.server_array[key].vm_array[i].NCPUs;

                proportion = ((np_aggregate.server_array[key].vm_array[i].RAM / np_aggregate.server_array[key].memory) * length);
                d_board.add_drawobj("rect","",shift_x + os,shift_y + offset_y + sofar,blockswide * blocksize, proportion * -1, colors[i], np_aggregate.server_array[key].vm_array[i],0);
                sofar = sofar - proportion;
            }
        }

        countx = countx + 1;
        if (countx > blockswide) {
        county = county + 1;
        countx = 0;
        }

        }
//d_board.listall();
        
        function animationLoop() {
        d_board.renderall();
        requestAnimationFrame(animationLoop);
        }
        requestAnimationFrame(animationLoop);
        </script>
    ''')
    tmpl_footer = Template(u'''\
	
        {% for x in range(1,node.processors) %}
            {{ x }}
    
        {% endfor %}
    
        {%- for vm in vm_array %}
            {{ vm.NCPU }}{% if not loop.last %},{% endif %}
        {%- endfor %}
    
        </body>
        </html>
        ''')
   

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
