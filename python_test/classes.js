function Aggregate() {
    this.server_array = [];
}
Aggregate.prototype.add_server = function(name, processors, memory, blockswide) {
    x = new Server(name, processors, memory, blockswide);
    this.server_array.push(x);
    return x 
}


function Server(name, processors, memory, blockswide){

    this.name = name;
    this.processors = processors;
    this.memory = memory;
    this.vm_array = [];
    this.blockswide = blockswide;
    this.array = [blockswide][Math.ceil(processors / blockswide)]
}

Server.prototype.add_vm = function(NCPU,RAM,STATE,HOST) {
    x = new VM(NCPU,RAM,STATE,HOST); 
    this.vm_array.push(x);
};

function VM(NCPU, RAM, STATE, HOST) {
    this.NCPU = NCPU;
    this.RAM = RAM;
    this.STATE = STATE;
    this.HOST = HOST;
}
