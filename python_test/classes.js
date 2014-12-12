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
    this.totalcpuusage = 0;
    this.totalramusage = 0;
    this.vm_array = [];
    this.blockswide = blockswide;
    this.array = [blockswide][Math.ceil(processors / blockswide)];
}

Server.prototype.add_vm = function(NCPU,RAM,STATE,HOST, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY_NAME) {
    x = new VM(NCPU,RAM,STATE,HOST,NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY_NAME); 
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
            context.strokeStyle = "black";
            context.fill();  
         }
         context.stroke();
     }

    if (this.type == "cross") {
         context.beginPath();
         context.moveTo(this.x,this.y);
         context.lineTo(this.w + this.x, this.h + this.y);
         context.moveTo(this.x,this.y + this.h);
         context.lineTo(this.x + this.w, this.y);
         context.strokeStyle = this.fillstyle;
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

        obj = this.layer_array[n].drawobj_array[i]; 

            //Don't process objects unless their y position is greater than the top of visible page portion
            if (obj.y + obj.h > top) { 

                    if (obj.y > top + bottom + 200 || obj.y + obj.h < top) {
                    exit = 1; 
                }       

            else {

                if (in_area(mouse_x, mouse_y, obj.x, obj.y, obj.w, obj.h)) {
                   board_x = 900; board_y = window.pageYOffset || document.documentElement.scrollTop + 20; 
                    if (obj.objdesc == "server_ram" || obj.objdesc == "server_cpu") { 
                        d_board.add_drawobj("rect","info","",board_x,board_y,500,500,"white",null,1); 
                        d_board.add_drawobj("text","info",obj.obj.name + ": ", board_x + 10,board_y + 15,0,0,"black",null,1);
                        d_board.add_drawobj("text","info","Memory Total: " + obj.obj.memory, board_x + 10,board_y + 30,0,0,"black",null,1);
                        d_board.add_drawobj("text","info","Memory Usage: " + obj.obj.totalramusage, board_x + 10,board_y + 45,0,0,"black",null,1);
                        d_board.add_drawobj("text","info","Memory Free: " + (obj.obj.memory - obj.obj.totalramusage), board_x + 10,board_y + 60,0,0,"black",null,1);
                        d_board.add_drawobj("text","info","Cores Total: " + (obj.obj.processors), board_x + 10,board_y + 75,0,0,"black",null,1);
                        d_board.add_drawobj("text","info","Cores Free: " + (obj.obj.processors - obj.obj.totalcpuusage), board_x + 10,board_y + 90,0,0,"black",null,1);


                        for (m = 0; m < obj.obj.vm_array.length; m++) {   
                            obj2 = obj.obj.vm_array[m];
                            d_board.add_drawobj("text","info","VM ID: " + obj2.UID + "STATE: " + obj2.STATE + "CORES: " + obj2.NCPU + "RAM: " + obj2.RAM,board_x + 10,board_y + 150 + 15 * m,0,0,"black",null,1);
                        }
                    }    
                    if (obj.objdesc == "cpu" || obj.objdesc == "ram") {
                        
                         d_board.add_drawobj("rect","info","",mouse_x,mouse_y,300,200,"orange",null,1); 
                    d_board.add_drawobj("text","info","Host: " + obj.obj.HOST,mouse_x + 5,mouse_y +15,0,0,"white",null,1);
                    d_board.add_drawobj("text","info","VM Name: " + obj.obj.NAME,mouse_x + 5,mouse_y +25,0,0,"white",null,1);
                    d_board.add_drawobj("text","info","VM ID:" + obj.obj.UID,mouse_x + 5,mouse_y + 35,0,0,"white",null,1);
                    d_board.add_drawobj("text","info","POWER STATE: " + obj.obj.STATE,mouse_x + 5,mouse_y + 45,0,0,"white",null,1);
                    d_board.add_drawobj("text","info","IMAGE: " + obj.obj.IMAGE,mouse_x + 5,mouse_y + 55,0,0,"white",null,1);
                    
                    d_board.add_drawobj("text","info","USER_ID: " + obj.obj.USER_ID,mouse_x + 5,mouse_y + 75,0,0,"white",null,1);
                    d_board.add_drawobj("text","info","TENANT_ID: " + obj.obj.TENANT_ID,mouse_x + 5,mouse_y + 85,0,0,"white",null,1);
                    
                    d_board.add_drawobj("text","info","CPUs: " + obj.obj.NCPU,mouse_x + 5,mouse_y + 95,0,0,"white",null,1);
                    d_board.add_drawobj("text","info","RAM: " + obj.obj.RAM,mouse_x + 5,mouse_y + 105,0,0,"white",null,1);
                    
                    d_board.add_drawobj("text","info","IP4: " + obj.obj.IP4,mouse_x + 5,mouse_y + 115,0,0,"white",null,1);
                    d_board.add_drawobj("text","info","KEY: " + obj.obj.KEY_NAME,mouse_x + 5,mouse_y + 125,0,0,"white",null,1);
                    
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


