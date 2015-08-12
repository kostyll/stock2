
var profile  = {
        user_setting:function(type, obj){
                 var value = "";
                 
                 if(obj.checked){
                        value = "yes";
                        $.ajax({
                                                url : "/profile/settings/"+type+"/"+value,
                                                type : 'GET', 
                                                dataType:'json',
                                                error : function(Data){
                                                        obj.checked = true;
                                                        Login.delete_g2a_session();
                                                },
                                                success : function(Data){
                                                        if(!Data["status"]){
                                                                my_alert("Что-то пошло не так, сообщите на support@btc-trade.com.ua  ");
                                                                obj.checked = false;
                                                        }else{
                                                                obj.checked = true;
                                                                my_alert("Настройки сохранены");
                                                                
                                                        }       
                                                }
                                        });
                        
                        
                 }else{                  
                          value = "no";
                          $.ajax({
                                                url : "/profile/settings/"+type+"/"+value,
                                                type : 'GET', 
                                                dataType:'json',
                                                error : function(Data){
                                                        obj.checked = true;
                                                        Login.delete_g2a_session();
                                                },
                                                success : function(Data){
                                                        if(!Data["status"]){
                                                                my_alert("Что-то пошло не так, сообщите на support@btc-trade.com.ua  ");
                                                                obj.checked = true;
                                                        }else{
                                                                obj.checked = false;
                                                                my_alert("Настройки сохранены");
                                                                
                                                        }       
                                                }
                                        });
                 }
                
                
                
        },
        user_g2a: function(type, obj){
                 var value = "";
                 if(!obj.checked){
                                obj.checked = true;
                                var turning_off_ga2 = function(ga2_Session){
                                                                                
                                        $.ajax({
                                                url : "/profile/settings/g2a/no",
                                                type : 'GET', 
                                                dataType:'json',
                                                error : function(Data){
                                                        obj.checked = true;
                                                        Login.delete_g2a_session();
                                                },
                                                success : function(Data){
                                                        if(!Data["status"]){
                                                                my_alert(Data["ru_description"]);
                                                                obj.checked = true;
                                                        }else{
                                                                obj.checked = false;
                                                                my_alert("Двухфакторная авторизация выключена");
                                                                
                                                        }       
                                                }
                                        });
                                };
                                return      Login.start_f2a_for_custom(turning_off_ga2);         
                } 
                
                $("#g2a_pwd").val("");                
                $.ajax({
                        url : "/profile/setup_g2a",
                        type : 'GET', 
                        dataType:'json',                        
                        error: function (data) {
                               my_alert("Что-то пошло не так, сообщите на support@btc-trade.com.ua  ");
                               obj.checked = false;
                        }, 
                        success : function(Data){
                                $('#g2a_private_key32').val(Data["g2a_private_key32"])
                                $('#g2a_private_key').val(Data["g2a_private_key"])
                                $('#g2a_qr').attr("src", Data["g2a_qr"] )
                                $('#f2a_dlg').modal('show'); 
                                obj.checked = false;
                                
                                
                        }
                        
                });
                                       
        },
        
        
        check_g2a:function(){
                var obj = document.getElementById("g2a_setting");
                var Value = $("#g2a_pwd").val()
                $.ajax({
                        url : "/profile/setup_g2a_verify/"+Value,
                        type : 'GET', 
                        dataType:'json',                        
                        error: function (data) {
                                my_alert("Пароль не подходит!!!");
                        }, 
                       success : function(Data){
                               $('#f2a_dlg').modal('hide') 

                                my_alert("Двухфакторная авторизация удачно установлена, теперь  \n\
                                          при следующей авторизации мы спросим у вас пароль из приложения. \n\
                                          Что бы отключить двухфакторную авторизацию достаточно снять флажок \n\
                                          в настройках вашего профиля.\n\
                                          ")
                                obj.checked = true;
                                
                                
                        }
                        
                });
                
                
                
        },
        reset_passwd:function(){
                 
                 $.ajax({
                        url : "/forgot_action",
                        type : 'GET', 
                        dataType:'json',                        
                        error: function (data) {
                               my_alert("Что-то пошло не так, сообщите на support@btc-trade.com.ua  ");
                        }, 
                        success : function(Data){
                                if(Data["status"]){
                                      my_alert("Новый пароль выслан на ваш электронный адрес");
                                      
                                }else{
                                      my_alert("Не получилось обновить пароль, попробуйте позже");
                                        
                                }       
                        }
                        
                });
                
        }
        
}