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


function DrawObj(type, text, x, y, w, h, fillstyle, obj, context) {
    this.type = type;
    this.text = text;
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.fillstyle;
    this.obj = obj;
    this.context = context;

}
DrawObj.prototype.render() {
   
     if (this.type == "rect") {
         this.context.beginPath();
         this.context.rect(this.x,this.y,this.w,this.h);
         this.context.fillStyle = this.fillstyle;
         this.context.fill(); 
     }
    
     if (this.type == "text") {
         this.context.fillStyle = this.fillstyle;
         this.context.fillText(this.text,this.x, this.y);

     }
    
}

funtion DrawingBoard() {
    this.drawobj_array = [];
    var canvas = document.getElementById('myCanvas');
    this.canvas = canvas;    
    var context = canvas.getContext('2d');
    this.context = context;
}


DrawingBoard.prototype.add_drawobj(type, text, x, y, h, w, fillstyle, object, context) {
    x = new DrawObj(type, text, x, y, h, w, fillstyle, object, context);
    this.drawobj_array.push(x)
}

DrawingBoard.prototype.renderall() {
    for (i = 0; i < this.drawobj_array.length; i++) {
        this.drawobj_array[i].render();
    }
}
