var Pins  = {
     host: "https://bitmoney.trade",
     host_ws: "wss://bitmoney.trade",
     id: "",
     container:"",
     session:"",
     is_delete: false,
     ws:null,
     is_availible:false,
     mutex_busy:false,
     attach2pin:function(identifier, container){
             if(Login.use_f2a)
                     return ;
             if(!document.getElementById(identifier))
                     return
                     
             Pins.id = identifier;
             Pins.container = container;
             var Res = $.ajax({
                              url : Pins.host + "/codes/start/12312asdasar34asda12",
                              type : 'GET',
                              cache: false,
                              error: function (data) {
                                    my_alert("Мы потеряли связь  с сервером перегрузите страницу, если не помогло обратитесь в службу поддержки");
                               },      
                               success : function(Data){
                                  $("#"+container).html( Data ); 
                                  Pins.session = $("#secure_pin_session").val();
                                  $("#"+ Pins.id).val(Pins.session);
                                  Pins.start_pin_listener(Pins.session);
                               }
                         });
             
     },
     start_pin_listener:function(Session){
             
        console.log('Connection');
        Pins.ws = new WebSocket(Pins.host_ws + "/command/" + Session);

        Pins.ws.onopen = function() {

            Pins.is_availible = true;
            console.log('Connected');
        };
        Pins.ws.onmessage = function (evt)
        {
            Pins.mutex_busy = false;
            var received_msg = evt.data; 
            var myObject = eval('(' + received_msg + ')');    
            console.log("Received: " + received_msg);
            if(Pins.is_delete){
                Pins.is_delete = false;
                if(myObject["status"]){
                        var val = $("#secure_pincode").val();
                        $("#secure_pincode").val( val.substring(0, val.length-1) );
                }                 
            }else{
                var val = $("#secure_pincode").val();
                if(myObject["status"]){
                        $("#secure_pincode").val(val + "*");                   
                }        
            }
            
            
            


        };
        Pins.ws.onclose = function()
        {
            Pins.is_availible = false;    
            my_alert("Мы потеряли связь  с сервером PIN -паролей перегрузите страницу, если не помогло обратитесь в службу поддержки");
            
        };
        
             
             
             
     },
     another_codes:function(){
         Pins.ws.onclose = null
         Pins.ws.close();
         Pins.attach2pin(Pins.id, Pins.container);
               
     },
     put_pin_key:function(obj){
                if(!Pins.is_availible)
                  my_alert("Мы потеряли связь  с сервером перегрузите страницу, если не помогло обратитесь в службу поддержки");
             
                var val = obj.id;
                if(Pins.mutex_busy)
                        return ;
                val = val.replace("pin_but_","");
                Pins.mutex_busy = true;
                js_txt =  JSON.stringify({
                                "new_key": val });
                                        
                console.log("send " + js_txt);
   
                Pins.ws.send(
                                js_txt
                            );
             
     },
     del_pin_key:function(){
              
            if(!Pins.is_availible)
                my_alert("Мы потеряли связь  с сервером перегрузите страницу, если не помогло обратитесь в службу поддержки");
                         
              
              
              if(Pins.mutex_busy)
                        return ;
              console.log("delete");              
              Pins.mutex_busy = true;              
              Pins.is_delete = true;
              Pins.ws.send(
                                JSON.stringify({
                                "del_key": true
                                })
                          );
    
    }       

        
        
}
