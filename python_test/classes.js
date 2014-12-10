function Aggregate() {
    this.server_array = [];
}
Aggregate.prototype.add_server = function(name, processors, memory, blockswide) {
    x = new Server(name, processors, memory, blockswide);
    this.server_array.push(x);
    return x; 
};


function Server(name, processors, memory, blockswide) {

    this.name = name;
    this.processors = processors;
    this.memory = memory;
    this.vm_array = [];
    this.blockswide = blockswide;
    this.array = [blockswide][Math.ceil(processors / blockswide)];
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


function DrawObj(type, text, x, y, w, h, fillstyle, obj) {
    this.type = type;
    this.text = text;
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.fillstyle = fillstyle;
    this.obj = obj;

}

DrawObj.prototype.render = function(context) {
   
     if (this.type == "rect") {
         context.beginPath();
         context.rect(this.x,this.y,this.w,this.h);
         if (this.fillstyle != "null") {
            context.fillStyle = this.fillstyle;
            context.fill();  
         }
         context.stroke();
     }
    
     if (this.type == "text") {
         context.fillStyle = this.fillstyle;
         context.fillText(this.text,this.x, this.y);
     }
    
};

function DrawingBoard() {
  
    var canvas = document.getElementById('myCanvas');
    this.drawobj_array = [];
    
    this.canvas = canvas;    
    var context = canvas.getContext('2d');
    this.context = context;
}


DrawingBoard.prototype.add_drawobj = function(type, text, x, y, h, w, fillstyle, object) {
    y = new DrawObj(type, text, x, y, h, w, fillstyle, object);
    this.drawobj_array.push(y);
};

DrawingBoard.prototype.renderall = function() {
    for (i = 0; i < this.drawobj_array.length; i++) {
        this.drawobj_array[i].render(this.context);
    }
};

DrawingBoard.prototype.listall = function() {
    for (i = 0; i < this.drawobj_array.length; i++) {
        a = this.drawobj_array[i].type;
        b = this.drawobj_array[i].text;
        c = this.drawobj_array[i].x;
        d = this.drawobj_array[i].y;
        e = this.drawobj_array[i].w;
        f = this.drawobj_array[i].h;
        g = this.drawobj_array[i].fillstyle;
        
        
        
        this.context.fillText(a + "," + b + "," + c + "," + d + "," + e + "," + f + "," + g, 10,1000 +i * 20);

    }
};


