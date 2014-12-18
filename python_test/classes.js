function Aggregate() {
    this.loaded = 0;
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

Server.prototype.add_vm = function(NCPU,RAM,STATE,HOST, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY_NAME, INSTANCE_NAME) {
    x = new Instance(NCPU,RAM,STATE,HOST,NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY_NAME, INSTANCE_NAME); 
    this.vm_array.push(x);
};

function Instance(NCPU, RAM, STATE, HOST, NAME, UID, CREATED, IP4, VOLUME, TENANT_ID, USER_ID, IMAGE, SECURITY, KEY_NAME, INSTANCE_NAME) {
    this.NCPU = NCPU;
    this.RAM = RAM;
    this.STATE = STATE;
    this.HOST = HOST;
    this.NAME = NAME;
    this.UID = UID;
    this.INSTANCE_NAME = INSTANCE_NAME;
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
    this.x = Math.floor(x);
    this.y = Math.floor(y);
    this.w = Math.floor(w);
    this.h = Math.floor(h);
    this.fillstyle = fillstyle;
    this.obj = obj;

}

DrawObj.prototype.render = function(context) {
   
     if (this.type == "rect_nofill") {
        context.strokeStyle = this.fillstyle;
        context.strokeRect(this.x,this.y,this.w,this.h); 
     }
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
    if (h < 0) {
    a = Boolean(x1 > x && x1 < x + w);
    b = Boolean(y1 > y + h && y1 < y);
    }
    else {
    a = Boolean(x1 > x && x1 < x + w);
    b = Boolean(y1 > y && y1 < y + h);
    }
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
 d_board.add_drawobj("text","framerate","FPS: " + fps,700, window.pageYOffset + window.innerHeight - 100,0,0,"black",null,1);



for (n = 0; n < this.layer_array.length; n++) {

        var top  = window.pageYOffset || document.documentElement.scrollTop,
        left = window.pageXOffset || document.documentElement.scrollLeft;
        right =  window.innerWidth;
        bottom = window.innerHeight;


       if (n == 0) {
            this.context.clearRect ( 0 , 0 , this.canvas.width, this.canvas.height );

       }



        exit = 0;
        for (i = 0; (i < this.layer_array[n].drawobj_array.length && exit == 0); i++) {

        obj = this.layer_array[n].drawobj_array[i]; 

            //Don't process objects unless their y position is greater than the top of visible page portion
            if (obj.y > top - 200) { 

           // If we've left the visible portion of the screen, exit the loop   
                if (obj.y > top + bottom + 180 || obj.y + obj.h < top - 200) {
                  //  exit = 1; 
                        r = 4;
               }       

               else {
                this.layer_array[n].drawobj_array[i].render(this.context);
                
                if (in_area(mouse_x, mouse_y, obj.x, obj.y, obj.w, obj.h) && n == 0) {

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
                      

                        if (obj.objdesc == "ram" || obj.objdesc == "cpu") {
                        
                        d_board.add_drawobj("rect_nofill","highlight","",obj.x,obj.y,obj.w,obj.h,"white",null,1);                          

                         if (info_lastobj != obj.obj) { 

                            info_lastobj = obj.obj;

                            info_x = mouse_x + 10;
                            document.getElementById("info").innerHTML = "Host: " + obj.obj.HOST + "<br>" + "<br>" +
                            "VM Name: " + obj.obj.NAME + "<br>" +
                            "VM ID:" + obj.obj.UID + "<br>" + 
                            "INSTANCE_NAME:" + obj.obj.INSTANCE_NAME + "<br>" +
                            "VM STATE: " + obj.obj.STATE + "<br>" +  
                            "IMAGE: " + obj.obj.IMAGE + "<br>" +
                            "USER_ID: " + obj.obj.USER_ID + "<br>" +
                            "TENANT_ID: " + obj.obj.TENANT_ID + "<br>" +               
                            "CPUs: " + obj.obj.NCPU + "<br>" +
                            "RAM: " + obj.obj.RAM + "<br>" +                  
                            "IP4: " + obj.obj.IP4 + "<br>" +
                            "KEY: " + obj.obj.KEY_NAME + "<br>"; 
                    
                         }
                        }

                }
            
             }   
           }       
        }
      }       
   }


DrawingBoard.prototype.renderall = function() {
   
    for (n = 0; n < this.layer_array.length; n++) {
            
   
    var top  = window.pageYOffset || document.documentElement.scrollTop,
    left = window.pageXOffset || document.documentElement.scrollLeft;
    right =  window.innerWidth;
    bottom = window.innerHeight;
    exit = 0;
  
     if (n == 0) {
    this.context.clearRect ( 0 , 0 , this.canvas.width, this.canvas.height );
}



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


