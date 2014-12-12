class Instance:
    NCPU = 0
    RAM = 0
    STATE = ""
    HOST = ""
    def __init__(self,NCPU,RAM,STATE,HOST, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY_NAME):
        self.NCPU = NCPU
        self.RAM = RAM
        self.STATE = STATE
        self.HOST = HOST
        self.NAME = NAME
        self.UID = UID
        self.CREATED = CREATED
        self.IP4 = VOLUME
        self.TENANT_ID = TENANT_ID
        self.USER_ID = USER_ID
        self.IMAGE = IMAGE
        self.SECURITY = SECURITY
        self.KEY_NAME = KEY_NAME

class Server:
    processors = 0
    memory = 0
    host = 0
    def __init__(self,host, processors, memory):
            
            self.vm_array = [ ]
    
            self.processors = processors
            self.memory = memory
            self.host = host
    def add_vm(self,NCPU, RAM, STATE, HOST, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY_NAME):
            x = Instance(NCPU,RAM,STATE,HOST, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY_NAME)
            self.vm_array.append(x)

class Aggregate:
    def __init__(self, hostlist, processors, memory):
        self.server_array = [ ]
        for host in hostlist:
            x = Server(host,processors,memory)
            self.server_array.append(x)


