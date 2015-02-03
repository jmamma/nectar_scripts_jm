
$( document ).ajaxStart(function() {
        $( "#loading" ).show();
});

$( document ).ajaxStop(function() {
        $( "#loading" ).hide();
});



function bugLoop() {
        bugcontext.clearRect ( 0 , 0 , bugcanvas.width, bugcanvas.height );
        chase.x = 50 * Math.cos(chase.angle) + 100;
        chase.y = 50 * Math.sin(chase.angle) + 100;
        chase.angle = chase.angle + .01;
    
    for (var n = 0; n < bugs.length; n++) {
        var bug = bugs[n];


        opposite = bug.y - chase.y; 
        adjacent = bug.x - chase.x;

        theta = Math.abs(Math.atan(opposite/adjacent));
        
        mag = Math.sqrt(Math.pow(opposite,2) + Math.pow(adjacent,2));


        bug.vx = Math.abs(bug.v * Math.sin(theta));
        bug.vy = Math.abs(bug.v * Math.cos(theta)); 
        if (opposite > 0) {
        bug.x = bug.x + bug.vx;
        } 
        else {
        bug.x = bug.x - bug.vx;
        }       
        if (adjacent > 0) {
        bug.y = bug.y - bug.vx;    
        }
        else {
        bug.y = bug.y + bug.vy;
        }
        
        bugcontext.strokeRect(bug.x, bug.y, 1,2); 

    }
       // bugcontext.strokeRect(chase.x, chase.y, 10,10); 
    
requestAnimationFrame(bugLoop);

}




function bug_load() {
    chase = { x:0, y:0, angle:0 }
    bugcanvas = document.getElementById('bugcanvas');
    bugcontext = bugcanvas.getContext('2d');        
    bugs = [];
    for (var n = 0; n < 400; n++) {
    var bug = { x:Math.floor(Math.random() * 450), y:Math.floor(Math.random() * 450), vx:Math.random() * 1, vy:Math.random(), v:1 };
    bugs.push(bug);
    }
        requestAnimationFrame(bugLoop);
    
}

function load() {

//Global variables in javascript have no var definition, even when assigned within functions.

colors = [ 'red', 'yellow', 'green', 'blue', 'pink', 'orange', 'purple', 'skyblue', 'violet', 'chocolate', 'firebrick', 'indigo', 'indianred', 'khaki', 'navy', 'olive', 'tan', 'coral', 'cornsilk', 'crimson', 'darkcyan', 'moccasin'];
offset_x = 25;
offset_y = 25;
length = 200;
blocksize = 20;
blockswide = 4; 
overextend = 32;
blocksize = (length) * blockswide / (24 + overextend) ;
cur_aggregate = new Aggregate();
d_board = new DrawingBoard();
cloud = new Cloud(); 
fps = 0;
d = new Date(); 
time_old = d.getTime(); 
frame_count = 0;
context = d_board.context;
d_board.add_layer();
d_board.add_layer();

//bug_load();

loadAggregates();
loadCloud('nectar!melbourne!qh2@netapp');
requestAnimationFrame(animationLoop);
}

var loadCloudAttempts = 0;


function loadAggregates() {
    $.getJSON("get_aggregates.py", function(result) {
 
    $.each(result, function(index,value) { 
        switch(index) { 
            case "aggregates":
               var cloud = new Cloud(); 
               cloud.aggregates = value;
                for (i = 0; i < cloud.aggregates.length; i++) {
                    agg = cloud.aggregates[i];
                    var select = document.getElementById("aggregates"); 
                    var el = document.createElement("option");
                    el.textContent = agg;
                    el.value = agg;
                    select.appendChild(el);
                } 
            break;
        } 
    });
 });

 }

function loadCloud(agg) {

$.getJSON("get_cloud.py", { aggregate: agg  },function(result) {
    alert("okay");

    $.each(result, function(index, value)  {
                            
            switch(index) {
                    case "server_array":
                    cur_aggregate.server_array = value;

                    break;
            }                
                    
                    generateCloud();

                                         }); 

                    });

 }



function loadCloud2(aggregate) {
alert(aggregate);
$.getJSON("get_cloud.py", { aggregate: aggregate  }, function(result) {
        alert(result);
     $.each(result, function(index, value)  {
        alert(index);
        switch(index) {
            case "server_array":
                alert(value[10].host);
                for (i = 0; i < value.length; i++) {
                cur_aggregate.add_server(value[i].host, value[i].processors, value[i].memory, 4);
                }

            break;
        }
generateCloud();

    }); 

});

}



var info_lastobj = null; 

function generateCloud() {

    d_board.clearall();
 countx = 0;
 county = 0;

 key = 0;
 alert(cur_aggregate.server_array.length);
 for (key = 0; key < cur_aggregate.server_array.length; key++) {

     shift_x = (blockswide * blocksize * 2 + offset_x * 2) * countx; 
     shift_y = (length + offset_y * 2) * county;


     d_board.add_drawobj("text","heading", cur_aggregate.server_array[key].host, offset_x + shift_x, offset_y / 2 + shift_y, 0, 0, "black", cur_aggregate.server_array[key],0);

     d_board.add_drawobj("rect","server_cpu", "", offset_x + shift_x,offset_y + shift_y + length,blockswide * blocksize, -1 * blocksize * 24 / blockswide, "lime", cur_aggregate.server_array[key],0);
     context.stroke();

     for (y = 0; y < (cur_aggregate.server_array[key].processsors) / blockswide; y++) {
         for (x = 0; x < blockswide; x++) {

 //    d_board.add_drawobj("rect", "cpu", "",shift_x + offset_x + x * blocksize,shift_y + offset_y + y * blocksize, blocksize, blocksize, "null", cur_aggregate.server_array[key],0);
         }
     }

     os = offset_x + blockswide * blocksize + offset_x;

     d_board.add_drawobj("rect","server_ram","", os + shift_x,offset_y + shift_y,blockswide * blocksize, length, "lime", cur_aggregate.server_array[key],0);

     sofar=length;
     coresleft = cur_aggregate.server_array[key].processors;

     x = 0
     y = 0
     
     totalramusage = 0;
     totalcpuusage = 0;
     //Iterate through each node/server to

     for (i = 0; i < cur_aggregate.server_array[key].vm_array.length; i++) {
                     
             cores = cur_aggregate.server_array[key].vm_array[i].NCPU;

             //Draw the individual Cores    
             for (n = cores; n > 0; n--) {
                 d_board.add_drawobj("rect","cpu","", shift_x + offset_x + (x * blocksize),shift_y + offset_y + length - (blocksize * (y + 1)), blocksize ,blocksize, colors[i], cur_aggregate.server_array[key].vm_array[i],0);
     
                 if (cur_aggregate.server_array[key].vm_array[i].STATE != "active") {
                    d_board.add_drawobj("cross","cpu","",shift_x + offset_x + (x * blocksize),shift_y + offset_y + length - (blocksize * (y + 1)), blocksize ,blocksize, "white", cur_aggregate.server_array[key].vm_array[i],0);
                 }
                 x = x + 1;
             
                 if (x >= blockswide) {
                  x = 0;  
                  y = y + 1;
                 }

              }
             
             //Draw the Memory

            // if (cur_aggregate.server_array[key].vm_array[i].STATE != "suspended") {  

             coresleft = coresleft - cur_aggregate.server_array[key].vm_array[i].NCPUs;

             proportion = ((cur_aggregate.server_array[key].vm_array[i].RAM / cur_aggregate.server_array[key].memory) * length);
             d_board.add_drawobj("rect","ram","",shift_x + os,shift_y + offset_y + sofar,blockswide * blocksize, proportion * -1, colors[i], cur_aggregate.server_array[key].vm_array[i],0);
         
             if (cur_aggregate.server_array[key].vm_array[i].STATE != "active") {
                 d_board.add_drawobj("cross","ram","",shift_x + os,shift_y + offset_y + sofar,blockswide * blocksize, proportion * -1, "white", cur_aggregate.server_array[key].vm_array[i],0);

             }
         
             sofar = sofar - proportion;
             totalramusage = totalramusage + cur_aggregate.server_array[key].vm_array[i].RAM;
             totalcpuusage = totalcpuusage + cur_aggregate.server_array[key].vm_array[i].NCPU;
             
            //  }
             
             cur_aggregate.server_array[key].totalramusage = totalramusage;
             cur_aggregate.server_array[key].totalcpuusage = totalcpuusage;
 
     }    

     //Calculate the horizontal shift for nodes

     countx = countx + 1;
     if (countx > blockswide) {
         county = county + 1;
         countx = 0;
     }

 }
cur_aggregate.loaded = 1;

}
//d_board.listall();
 
var mouse_x = 0, mouse_y = 0;
 
function updateMouse(event) {
     mouse_x = event.clientX +  window.pageXOffset || document.documentElement.scrollLeft;
     mouse_y = -100 + event.clientY  + window.pageYOffset || document.documentElement.scrollTop;
}

function animationLoop() {
     d = new Date(); 
     time_new = d.getTime();
     frame_count = frame_count + 1;
//            fps = time_new - time_old;
     if (time_new - time_old > 1000) {
         fps = frame_count;
         frame_count = 0;
         time_old = d.getTime(); 
      }

      if (cur_aggregate.loaded == 1) { 
         d_board.checkmouse();
     } 
// d_board.renderall();
     requestAnimationFrame(animationLoop);
}


