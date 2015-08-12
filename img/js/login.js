
var Login =  {
       logged:false,
       after_redirect:false,
       custom_auth_action: null,
       use_f2a: false,
       sessionid:null,
       keyup:function(event){
                if(event.keyCode == 13){
                        Login.try_login_page();
                        
                }       
               
        },       
        f2a_keyup:function(event){
                if(event.keyCode == 13){
                        Login.f2a_try_login();
                        
                }   
        },
        f2a_custom_keyup:function(event){
                if(event.keyCode == 13){
                        Login.f2a_custom_action();
                }   
        },
        login:function(){
                $("#login_form").show("fast");      
        },
        try_login_page: function(){
               var login = $("#login_username").val();
               var password = $("#login_password").val();
               Login.post_url = $("#post_url").val(); 
               Login.after_redirect = true;
               console.log(Login.post_url);
               var Data = {"login":login, "password":password }; 
               $.ajax({
                        url : "/login?_=" + Date(),
                        data: Data,
                        type : 'POST', 
                        success : function(data){
                                var patt = new RegExp("good");
                                if(patt.test(data)){
                                        Login.logged = true;
                                        if(Login.post_url && Login.post_url.length > 0){
                                                window.location.href = Login.post_url;
                                        }else{
                                                window.location.href="/stock";
                                        }        
                                        return 
                                        
                                }
                                var patt = new RegExp("2fa_");
                                if(patt.test(data)){
                                        
                                        Login.f2a_start(data);
                                        return 
                                        
                                }
                                
                                my_alert("Не удалось авторизироваться");
                                        
                                
                        }
                });

               
       },
       f2a_try_login:function(){
               
               var password  =$('#f2a_password').val();
               var session = $('#f2a_session').val();
               var Data = {"key":session, "password":password };                  
               $.ajax({
                        url : "/login_f2a?_=" + Date(),
                        data: Data,
                        type : 'POST', 
                        error: function (data) {
                                                console.log(data);
                                                $('#f2a_password').val("");
                                                my_alert("Не могу авторизироваться")
                        }, 
                        success : function(data){
                                var patt = new RegExp("good");
                                if(patt.test(data)){
                                        Login.logged = true;
                                        if(Login.after_redirect){
                                             if(Login.post_url && Login.post_url.length > 0){
                                                        window.location.href = Login.post_url;
                                             }else{
                                                        window.location.href="/stock";
                                             }    
                                             return 
                                        }
                                        else{
                                             $("#f2a_dlg_login").modal("hide");
                                             Login.load_user_panel();
                                                
                                        }
                                        return ;
                                }
                                my_alert("Не удалось авторизироваться");
                                        
                                
                        }
                });
               
       },
       f2a_start: function(Session){
               $('#f2a_session').val(Session);
               $('#f2a_dlg_login').modal('show'); 
               
               
               
       },
       start_f2a_for_custom: function(custom_action){
               console.log(Login.use_f2a);
               if(Login.use_f2a){
                        Login.delete_g2a_session();
                        $("#f2a_dlg_custom").modal('show');                            
                        Login.custom_auth_action = custom_action;                
               }else{
                        custom_action("f2a");
               }
                       
       },
       f2a_custom_action:function(){
               var password  = $('#f2a_custom_password').val();
               var Data = { "password":password };     
               Date
               $.ajax({
                        url : "/login_f2a_operation?_=" + Date(),
                        data: Data,
                        type : 'POST', 
                        error: function (data) {
                                                console.log(data);
                                                $('#f2a_custom_password').val("");
                                                my_alert("Не могу авторизироваться")
                        }, 
                        success : function(data){
                                
                                 $("#f2a_dlg_custom").modal('hide');
                                 Login.setup_g2a_session(data);
                                 Login.custom_auth_action(data)               
                                
                        }
                });
       },     
       setup_g2a_session: function(data){
          $.cookie("g2a_session", data, {
                expires : 1,           
                path    : '/',          
                secure  : true         
             });
                        
        },
        delete_g2a_session:function(){
                $.removeCookie("g2a_session");
                
        },
       try_login: function(){
               var login = $("#login_username").val();
               var password = $("#login_password").val();
               var Data = {"login":login, "password":password };                  
               $.ajax({
                        url : "/login?_=" + Date(),
                        data: Data,
                        type : 'POST', 
                        success : function(data){
                                var patt = new RegExp("good");
                                if(patt.test(data)){
                                        Login.logged = true;
                                        Login.load_user_panel();
                                        return
                                }
                                var patt = new RegExp("2fa_");
                                if(patt.test(data)){
                                        Login.f2a_start(data);
                                        return 
                                }
                                
                                my_alert("Не удалось авторизироваться");
                                        
                        }
                });

               
       },
       
       
       load_user_panel:function(){
               $.ajax({
                        url : "/user_panel/" + Main.trade_pair,
                        type : 'GET', 
                        success : function(data){
                                var patt = new RegExp("bad");
                                if(patt.test(data)){
                                      my_alert("Что-то пошло не так");
                                }else{
                                     $("#user_panel").html(data);
                                     
                                     $("#buy_button").attr("disabled", false);
                                     $("#sell_button").attr("disabled", false);
                                     Main.user_menu();   
                                }       
                        }
                });
               
               
        }

        
};