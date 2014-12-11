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

Server.prototype.add_vm = function(NCPU,RAM,STATE,HOST, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY_NAME) {
    x = new VM(NCPU,RAM,STATE,HOST); 
    this.vm_array.push(x);
};

function VM(NCPU, RAM, STATE, HOST, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY_NAME) {
    this.NCPU = NCPU;
    this.RAM = RAM;
    this.STATE = STATE;
    this.HOST = HOST;
    this.NAME = NAME;
    this.UID = UID;
    this.CREATED = CREATED;
    this.IP4 = IP4;
    this.VOLUME = VOLUME;
    this.TENANT_ID = TENANT_ID;
    this.USER_ID = USER_ID;
    this.IMAGE = IMAGE;
    this.SECURITY = SECURITY;
    this.KEY_NAME = KEY_NAME;
}


function DrawObj(type, objdesc, text, x, y, w, h, fillstyle, obj) {
    this.type = type;
    this.objdesc = objdesc;
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

function Layer(context) {
    this.context = context;
    this.drawobj_array = [];
}

function DrawingBoard() {
  
    var canvas = document.getElementById('myCanvas');
    this.layer_array = [];
    
    this.canvas = canvas;    
    var context = canvas.getContext('2d');
    this.context = context;
}

DrawingBoard.prototype.add_layer = function() {
    z = new Layer(this.context);
    this.layer_array.push(z);
}

function in_area(x1, y1, x, y, w, h) {
    a = Boolean(x1 > x && x1 < x + w);
    b = Boolean(y1 > y && y1 < y + h);
    return Boolean(a && b);
}


DrawingBoard.prototype.add_drawobj = function(type, objdesc, text, x, y, h, w, fillstyle, object, layer) {
    y = new DrawObj(type, objdesc, text, x, y, h, w, fillstyle, object);
    this.layer_array[layer].drawobj_array.push(y);
};

DrawingBoard.prototype.checkmouse = function() {

        this.layer_array[1].drawobj_array.length = 0;
//        d_board.add_drawobj("text","yaaaaay",mouse_x,mouse_y,0,0,"black",null,1);
        n = 0;       
 
   var top  = window.pageYOffset || document.documentElement.scrollTop,
 left = window.pageXOffset || document.documentElement.scrollLeft;
 right =  window.innerWidth;
 bottom = window.innerHeight;

        exit = 0;
        for (i = 0; (i < this.layer_array[n].drawobj_array.length && exit == 0); i++) {
    
            //Don't process objects unless their y position is greater than the top of visible page portion
            if (this.layer_array[n].drawobj_array[i].y + this.layer_array[n].drawobj_array[i].h > top) { 

                    if (this.layer_array[n].drawobj_array[i].y > top + bottom + 200 || this.layer_array[n].drawobj_array[i].y + this.layer_array[n].drawobj_array[i].h < top) {
                    exit = 1; 
                }       

            else {

                if (in_area(mouse_x, mouse_y, this.layer_array[n].drawobj_array[i].x, this.layer_array[n].drawobj_array[i].y, this.layer_array[n].drawobj_array[i].w, this.layer_array[n].drawobj_array[i].h)) {
                
                    if (this.layer_array[n].drawobj_array[i].objdesc == "cpu") {
                        text = this.layer_array[n].drawobj_array[i].obj.HOST;
                         d_board.add_drawobj("rect","info","",mouse_x,mouse_y,100,30,"orange",null,1); 
                           d_board.add_drawobj("text","info",text,mouse_x + 5,mouse_y +15,0,0,"white",null,1);
                    
                    }

                }
            

            }   
        }       
        }       

        }


DrawingBoard.prototype.renderall = function() {
   
    for (n = 0; n < this.layer_array.length; n++) {
            
    if (n == 0) {
     this.context.clearRect ( 0 , 0 , this.canvas.width, this.canvas.height );
    }
    
    var top  = window.pageYOffset || document.documentElement.scrollTop,
    left = window.pageXOffset || document.documentElement.scrollLeft;
    right =  window.innerWidth;
    bottom = window.innerHeight;
    exit = 0;
    
    for (i = 0; (i < this.layer_array[n].drawobj_array.length && exit == 0); i++) {
   
        if (this.layer_array[n].drawobj_array[i].y + this.layer_array[n].drawobj_array[i].h > top) { 
        if (this.layer_array[n].drawobj_array[i].y > top + bottom + 200 || this.layer_array[n].drawobj_array[i].y + this.layer_array[n].drawobj_array[i].h < top) {
            exit = 1; 
        }

        else {
            this.layer_array[n].drawobj_array[i].render(this.context);
        }
        }
    }
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


