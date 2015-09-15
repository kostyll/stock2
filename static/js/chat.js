var Chat  = {
//      host: "https://btc-trade.com.ua/chat",
     host_ws: "wss://bitmoney.trade/chat",
     id: "",
     container:"",
     session:"",
     is_delete: false,
     timer: null,
     ws:null,
     username:null,
     is_availible:true,
     mutex_busy:false,
     last_post:null,
     attach2chat:function( container ){
        Chat.container = container;
        if(!document.getElementById(container))
                return;
        
        Chat.ws = new WebSocket(Chat.host_ws );
        Chat.is_availible = true;
        Chat.ws.onopen = function() {
            console.log('Connected');
            
            Chat.timer =  setInterval(Chat.ping, 3000);
            
        };
        Chat.ws.onmessage = function (evt)
        {
            var received_msg = evt.data; 
            var myObject = eval('(' + received_msg + ')');    
            console.log("Received: " + received_msg);
            
            if(myObject.status){
                var size = myObject.new_messages.length;
                var messages = myObject.new_messages;
                var NewElements = "";
                
                for(var i = 0; i< size;i++){
                                        var username =  messages[i]["username"];
                                        var message =  messages[i]["message"];
                                        
                                        var NewElement = "<tr class='cursor' onclick=\"answer('"+username+"')\">";                                                        
                                        NewElement  +="<td ><strong>"+ username  +"</strong>:&nbsp;</td></tr><tr><td>";
                                        NewElement  += message+"</td></tr>";
                                        NewElements += NewElement;
                }
                $("#"+Chat.container).prepend( NewElements );
            }

        };
        Chat.ws.onclose = function()
        {
            Chat.is_availible = false; 
            clearTimeout(Chat.timer);
            Chat.attach2chat(Chat.container);
            
        };
        
             
             
             
     },
     ping:function(){
             Chat.ws.send(
                     JSON.stringify({
                     "ping": true                                        
                    })
             );
             
     },
     put_message:function(Text){
                if(!Chat.is_availible){
                        my_alert("Мы потеряли связь  с сервером Чата");
                        return false
                }
                if(!Login.logged){
                       my_alert("Вы должны пройти процедуру авторизации, что бы писать в чат");
                }


                var session = Login.sessionid;
                if(Chat.last_post){
                        var  Seconds =  new Date();
                        Seconds =   Seconds.getTime() - Chat.last_post.getTime();
                        console.log("ofter " + Seconds)
                        if( Seconds<15000 ){
                                my_alert("Погодь не так часто, подумай что хочешь сказать");
                                return 
                        }
                }
                
                
                Chat.last_post = new Date();
                var val = Text;              
                console.log("send " + val);
                Chat.ws.send(
                                JSON.stringify({
                                "new_message": val,
                                "session": session
                                        
                                })
                            );
                return true
             
     }
       
        
}
function scroll_chat()
{
//         $("#chat_wrapper")[0].scrollTop($("#chat_wrapper")[0].scrollHeight);

        var scroll = $("#chat_wrapper").scrollTop();
        console.log("start scroll " + scroll);

        var cur_scroll =  scroll+$("#chat_wrapper").innerHeight();
        console.log("current scroll " + cur_scroll);
        var scroll_height=$("#chat_wrapper")[0].scrollHeight;
        console.log(" scroll height " + scroll_height);
        var obj  = $("#chat_wrapper")[0];
        obj.scrollTop =  scroll_height ;
//         cur_scroll>scroll_height-30-a?c?$("#nChatLockIcon").fadeOut(150):$("#chat_wrapper").scrollTop(scroll_height):c?$("#nChatLockIcon").fadeIn(150):0<b&&$("#nChat").scrollTop(scroll-b)
        
        
}

function send_message(){
        var Text  =$("#msg").val();
        if(Text == ""){
                return 
        }
        if(Chat.put_message(Text)){
                $("#msg").val("");
        }
        
}

function answer(Username){
        var Text = $("#msg").val();
        Text = Username +"," + Text;
        
        $("#msg").focus();
        $("#msg").val(Text);
        
}
   function createCookie(name, value, days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    } else var expires = "";
    document.cookie = escape(name) + "=" + escape(value) + expires + "; path=/";
}

function readCookie(name) {
        var nameEQ = escape(name) + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return unescape(c.substring(nameEQ.length, c.length));
        }
        return null;
    }

    function eraseCookie(name) {
        createCookie(name, "", -1);
    }
