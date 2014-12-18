 var colors = [ 'red', 'yellow', 'green', 'blue', 'pink', 'orange', 'purple', 'skyblue', 'violet', 'chocolate', 'firebrick', 'indigo', 'indianred', 'khaki', 'navy', 'olive', 'tan', 'coral', 'cornsilk', 'crimson', 'darkcyan', 'moccasin'];
 var offset_x = 25;
 var offset_y = 25;
 var length = 200;
 var blocksize = 20;
 var blockswide = 4; 
 var overextend = 32;
 blocksize = (length) * blockswide / (24 + overextend) ;
 var np_aggregate = new Aggregate();

 var d_board = new DrawingBoard();
 
 context = d_board.context;
 d_board.add_layer();
 d_board.add_layer();

 var loadCloudAttempts = 0;


 function loadCloud() {
 $.getJSON("get_cloud.py", function(result) {
     alert("okay");

      $.each(result, function(index, value)  {
 
         switch(index) {
             case "server_array":
              np_aggregate.server_array = value;

             alert("i am king");
             break;
         }
generateCloud();

     }); 

 });

 }

 loadCloud();
 var info_lastobj = null; 

 function generateCloud() {
 countx = 0;
 county = 0;

 key = 0;
 alert(np_aggregate.server_array.length);
 for (key = 0; key < np_aggregate.server_array.length; key++) {

     shift_x = (blockswide * blocksize * 2 + offset_x * 2) * countx; 
     shift_y = (length + offset_y * 2) * county;


     d_board.add_drawobj("text","heading", np_aggregate.server_array[key].host, offset_x + shift_x, offset_y / 2 + shift_y, 0, 0, "black", np_aggregate.server_array[key],0);

     d_board.add_drawobj("rect","server_cpu", "", offset_x + shift_x,offset_y + shift_y + length,blockswide * blocksize, -1 * blocksize * 24 / blockswide, "lime", np_aggregate.server_array[key],0);
     context.stroke();

     for (y = 0; y < (24 + overextend) / blockswide; y++) {
         for (x = 0; x < blockswide; x++) {

 //    d_board.add_drawobj("rect", "cpu", "",shift_x + offset_x + x * blocksize,shift_y + offset_y + y * blocksize, blocksize, blocksize, "null", np_aggregate.server_array[key],0);
         }
     }

     os = offset_x + blockswide * blocksize + offset_x;

     d_board.add_drawobj("rect","server_ram","", os + shift_x,offset_y + shift_y,blockswide * blocksize, length, "lime", np_aggregate.server_array[key],0);

     sofar=length;
     coresleft = np_aggregate.server_array[key].processors;

     x = 0
     y = 0
     
     totalramusage = 0;
     totalcpuusage = 0;
     //Iterate through each node/server to

     for (i = 0; i < np_aggregate.server_array[key].vm_array.length; i++) {
                     
             cores = np_aggregate.server_array[key].vm_array[i].NCPU;

             //Draw the individual Cores    
             for (n = cores; n > 0; n--) {
                 d_board.add_drawobj("rect","cpu","", shift_x + offset_x + (x * blocksize),shift_y + offset_y + length - (blocksize * (y + 1)), blocksize ,blocksize, colors[i], np_aggregate.server_array[key].vm_array[i],0);
     
                 if (np_aggregate.server_array[key].vm_array[i].STATE != "active") {
                    d_board.add_drawobj("cross","cpu","",shift_x + offset_x + (x * blocksize),shift_y + offset_y + length - (blocksize * (y + 1)), blocksize ,blocksize, "white", np_aggregate.server_array[key].vm_array[i],0);
                 }
                 x = x + 1;
             
                 if (x >= blockswide) {
                  x = 0;  
                  y = y + 1;
                 }

              }
             
             //Draw the Memory

             if (np_aggregate.server_array[key].vm_array[i].STATE != "suspended") {  

             coresleft = coresleft - np_aggregate.server_array[key].vm_array[i].NCPUs;

             proportion = ((np_aggregate.server_array[key].vm_array[i].RAM / np_aggregate.server_array[key].memory) * length);
             d_board.add_drawobj("rect","ram","",shift_x + os,shift_y + offset_y + sofar,blockswide * blocksize, proportion * -1, colors[i], np_aggregate.server_array[key].vm_array[i],0);
         
             if (np_aggregate.server_array[key].vm_array[i].STATE != "active") {
                 d_board.add_drawobj("cross","ram","",shift_x + os,shift_y + offset_y + sofar,blockswide * blocksize, proportion * -1, "white", np_aggregate.server_array[key].vm_array[i],0);

             }
         
             sofar = sofar - proportion;
             totalramusage = totalramusage + np_aggregate.server_array[key].vm_array[i].RAM;
             totalcpuusage = totalcpuusage + np_aggregate.server_array[key].vm_array[i].NCPU;
             
              }
             
             np_aggregate.server_array[key].totalramusage = totalramusage;
             np_aggregate.server_array[key].totalcpuusage = totalcpuusage;
 
     }    

     //Calculate the horizontal shift for nodes

     countx = countx + 1;
     if (countx > blockswide) {
         county = county + 1;
         countx = 0;
     }

 }
np_aggregate.loaded = 1;

 }
//d_board.listall();
 
 var mouse_x = 0, mouse_y = 0;
 
 function updateMouse(event) {
     mouse_x = event.clientX +  window.pageXOffset || document.documentElement.scrollLeft;
     mouse_y = -100 + event.clientY  + window.pageYOffset || document.documentElement.scrollTop;
 }

 fps = 0;
 d = new Date(); 
 time_old = d.getTime(); 
 frame_count = 0;

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

      if (np_aggregate.loaded == 1) { 
         d_board.checkmouse();
     } 
// d_board.renderall();
     requestAnimationFrame(animationLoop);
 }
 requestAnimationFrame(animationLoop);

