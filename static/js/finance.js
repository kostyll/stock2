
"use strict";

var server_name = "bitcoin trade company";


var finance  = {
        crypto_currency:
        {
                "NVC":1,"BTC":1,"LTC":1,"HIRO":1,"DRK":1,"VTC":1, "PPC":1,"DOGE":1,"CLR":1,"RMS":1,'NMC':1
        },
        order_id: "",
        min_deal: 0.00001,
        timer: null,
        liqpay_flag: false,
        p24_flag:false,
        p_flag:false,
        o_flag:false,
        ui_check_status:function(){
                        
                   $.ajax({
                              dataType: 'json',
                              url : "/api/order/status/" + finance.order_id,
                              type : 'GET', 
                              cache: false,
                              error: function (data) {
                                                console.log(data);
                                                my_alert("Не могу создать ордер  ")
                              }, 
                              success : function(Data){
                                               var status = Data["status"];
                                               if(status == "processed"){
                                                        $("#work_msg").html("<p>Средства удачно зачислены</p>");                                                        
                                                        window.location.href="/finance/balance";
                                                        clearTimeout(finance.timer);
                                                        return ;
                                               }
                                               if(status == "created"){
                                                        $("#work_msg").html("Cтатус платежа <font color=\"greed\" id=\"depo_status\">\
                                                                                  в обработке </font>");                                                        
                                                        return ;
                                                       
                                               }  
                                               if(status == "processing"){
                                                        $("#work_msg").html("Cтатус платежа <font color=\"greed\" id=\"depo_status\">\
                                                                                  в обработке </font>");                                                        
                                                        return ;
                                                       
                                               }  
                                               if(status == "wait_secure"){
                                                        $("#work_msg").html("<p>Ваша оплата была отправленна платежной системой на ручную обработку</p>\
                                                                                  <p>После проверки, ваши средства будут немедленно зачисленны</p>");
                                                        clearTimeout(finance.timer);
                                                        return ;        
                                               }
                                               if(status == "order_cancel"){
                                                        clearTimeout(finance.timer);
                                                        $("#work_msg").html("Ваша оплата была забракована платежной системой")
                                                        return ;
                                               }
                                               $("#work_msg").html("Что-то пошло не так, обратитесь в службу поддержки");
                                               clearTimeout(finance.timer);
                                               return ;                                              
                                                
                                         }
                              });      
                
                
                
        },
      
        
        make_deposit: function(Currency){
                $("#withdraw_form").css({"display":"none"});
                window.scrollTo(0, 0);
                $("#currency_depo").val(Currency);
                finance.fill_providers_depo(Currency);
                $("#deposit_form").slideDown("slow");
        },
        /*     <option value="">
                            Выбрать
              </option>
             <option  value="liqpay_transfer">
                        LiqPay
             </option>
              <option value="bank_transfer">
                                   Банковский перевод
               </option>*/
        fill_uah: function(){
                        $("#provider_depo").append( $('<option value="">Выбрать</option>') );
                        $("#provider_depo").append( $('<option value="liqpay_transfer">LiqPay Платежной Картой 2.75% для всех карт Visa,MasterCard </option>') );    
                        $("#provider_depo").append( $('<option value="liqpay_transfer">2.75% наличными в терминалах ПриватБанка </option>') );    
                        $("#provider_depo").append( $('<option value="p24_transfer">Через Приват24( 2% ) </option>') );                       
            
                        $("#label_depo").html( "Cпособ пополения:" );                       
                        $("#label_amnt_depo").show();                      
                        $("#amnt_depo").show();                       
                        $("#provider_depo").show();
          
            
            
        },
        fill_usd: function(){
                        $("#provider_depo").append( $('<option value="">Выбрать</option>') );
                        $("#provider_depo").append( $('<option value="perfect_usd">Perfect Money</option>') );    
                        $("#provider_depo").append( $('<option value="okpay_usd">OkPay</option>') );    
                        $("#provider_depo").append( $('<option value="payeer_usd">Payeer</option>') );  
                        $("#label_depo").html( "Cпособ пополения:" );                       
                        $("#label_amnt_depo").show();                      
                        $("#amnt_depo").show();                       
                        $("#provider_depo").show();
          
            
            
        },
        fill_eur: function(){
                        $("#provider_depo").append( $('<option value="">Выбрать</option>') );
                        $("#provider_depo").append( $('<option value="perfect_eur">Perfect Money</option>') );    
                        $("#provider_depo").append( $('<option value="okpay_eur">OkPay</option>') );    
                        $("#provider_depo").append( $('<option value="payeer_eur">Payeer</option>') );
                        $("#label_depo").html( "Cпособ пополения:" );                       
                        $("#label_amnt_depo").show();                      
                        $("#amnt_depo").show();                       
                        $("#provider_depo").show();
        },
        fill_rur: function(){
                        $("#provider_depo").append( $('<option value="">Выбрать</option>') );
                        $("#provider_depo").append( $('<option value="yandex_rur">Yandex</option>') );  
                        $("#provider_depo").append( $('<option value="okpay_rur">OkPay</option>') );    
                        $("#provider_depo").append( $('<option value="payeer_rur">Payeer</option>') );  
                        $("#label_depo").html( "Cпособ пополения:" );                       
                        $("#label_amnt_depo").show();                      
                        $("#amnt_depo").show();                       
                        $("#provider_depo").show();
        },
        
        fill_providers_depo:function(Currency){
                $("#provider_depo").html("");
                $("#res_provider").html("")

                if(!finance.crypto_currency[Currency]){
                    
                     if(Currency=="UAH")
                        finance.fill_uah();
                     
                     if(Currency=="USD")
                        finance.fill_usd();
                     
                     if(Currency=="EUR")
                        finance.fill_eur();
                     
                     if(Currency=="RUR")
                        finance.fill_rur();
                        

                }
                
                if(finance.crypto_currency[Currency]){
                        $("#provider_depo").hide();
                        $("#label_depo").html( "Кошелек пополения:" );                       
                        $("#label_amnt_depo").hide();                      
                        $("#amnt_depo").hide();                       

                        $.ajax({
                                        url : "/finance/crypto_currency/"+Currency,
                                        type : 'GET',
                                        dataType: "json",
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider").html( "permission denied" );  
                                                my_alert("Проблемы в работе с кошельком обратитесь в support@"+server_name);       
                                                $("#provider_depo").val("");
                                                return  false;
                                        },      
                                        success : function(Data){
                                                   if(Data["account"]){    
                                                       $("#res_provider").html(
                                                               '<div class="col-sm-6"><strong>'+ 
                                                               Data["account"]+ '</strong></div>')
                                                           
                                                   }
                                         }
                                     });         
                        

                }                         
        },
        change_depo:function(obj){
                var provider = obj.value;
                
                if(provider == "")
                        return ;
                
                var currency = $("#currency_depo").val();
                var amnt =$("#amnt_depo").val(); 
                  
                if(provider == "bank_transfer")
                       return finance.bank_transfer(obj, amnt, currency )
                       
                if(provider == "liqpay_transfer")
                       return finance.liqpay_transfer(obj, amnt,  currency ) 
                       
                if(provider == "p24_transfer")
                       return finance.p24_transfer(obj, amnt,  currency )   
                       
                if(provider == "perfect_usd")
                       return finance.p_transfer(obj, amnt,  "USD" )
                
                if(provider == "perfect_eur")
                       return finance.p_transfer(obj, amnt,  "EUR" )
                
                if(provider == "okpay_usd")
                       return finance.okpay_transfer(obj, amnt,  "USD" )
                
                if(provider == "okpay_eur")
                       return finance.okpay_transfer(obj, amnt,  "EUR" )  
                
                if(provider == "okpay_rur")
                       return finance.okpay_transfer(obj, amnt,  "RUR" )  
                       
                if(provider == "ya_ru")
                       return finance.ya_transfer(obj, amnt )
                
                       
        },
        ya_transfer: function(obj, Amnt){
            if(currency != "RUR"){
                        obj.value = "";
                        my_alert("Неправильная валюта");       
                        return false;
                }
                if(Amnt<10){
                        obj.value = "";
                        my_alert("Ограничение минимальной суммы пополнения через Yandex Money");       
                        return false;
                }          
                var Res = $.ajax({
                                        url : "/finance/ya/deposit/"+currency+"/"+Amnt,
                                        type : 'GET',
                                        cache: false,
                                        error: function(data){
                                                $("#res_provider").html( "permission denied" );      
                                                obj.value = "";
                                        },      
                                        success : function(Data){
                                                   var comission = ""; //"<p class=\"help-block\">Комиссия за пополнение составляет 2% с карты ПриватБанка, 2% + 10 грн с карт других банков</p>";
                                                    $("#res_provider").html( comission + Data ); 
                                                    $("#ya_submit_button").css("margin-right","11em");
                                                    $("#ya_submit_button").attr("class","btn btn-success pull-right");
                                                    $("#pay_form").bind( "submit", function() {
                                                         return finance.o_flag;
                                                         //strange but not work without it
                                                    });
                                                   $("#ya_submit_button").bind( "click", finance.okpay_start);
                                                   
                                         }
                                     }); 
            
            
        },
        ya_start: function(obj, Amnt){
                var currency = $("#currency_depo").val();
                var amnt = $("#amnt_depo").val(); 
                
                if( currency != "RUR"){
                        $("#provider_depo").val("");
                        my_alert("Неправильная валюта");       
                        return false;
                }
                if(amnt<10){
                        $("#provider_depo").val("");
                        my_alert("Ограничение минимальной суммы пополнения через Yandex Money");       
                        return false;
                }          
                
                var Res = $.ajax({
                                        url : "/finance/ya/start/"+currency+"/"+amnt,
                                        type : 'GET',
                                        dataType: "json",
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider").html( "permission denied" );      
                                                $("#provider_depo").val("");
                                                return  false;
                                        },      
                                        success : function(Data){
                                                   if(Data["order_id"]){    
                                                        //$("#p_public_key").val(Data["public_key"]);         
                                                        $("#label").val(Data["order_id"]);         
                                                        $("#sum").val(Data["amount"]);                                                                 
                                                        finance.o_flag = true;
                                                        $("#pay_form").submit();                                            
                                                   }
                                         }
                                     });        
            
            
        },
        okpay_transfer: function(obj, Amnt, currency){
                if(currency != "USD" && currency != "EUR" && currency != "RUR"){
                        obj.value = "";
                        my_alert("Неправильная валюта");       
                        return false;
                }
                if(Amnt<10){
                        obj.value = "";
                        my_alert("Ограничение минимальной суммы пополнения через OkPay");       
                        return false;
                }          
                var Res = $.ajax({
                                        url : "/finance/okpay/deposit/"+currency+"/"+Amnt,
                                        type : 'GET',
                                        cache: false,
                                        error: function(data){
                                                $("#res_provider").html( "permission denied" );      
                                                obj.value = "";
                                        },      
                                        success : function(Data){
                                                   var comission = ""; //"<p class=\"help-block\">Комиссия за пополнение составляет 2% с карты ПриватБанка, 2% + 10 грн с карт других банков</p>";
                                                    $("#res_provider").html( comission + Data ); 
                                                    $("#ya_submit_button").css("margin-right","11em");
                                                    $("#ya_submit_button").attr("class","btn btn-success pull-right");
                                                    $("#pay_form").bind( "submit", function() {
                                                         return finance.o_flag;
                                                         //strange but not work without it
                                                    });
                                                   $("#ya_submit_button").bind( "click", finance.okpay_start);
                                                   
                                         }
                                     });   
                
        },
        okpay_start:function(){
                var currency = $("#currency_depo").val();
                var amnt = $("#amnt_depo").val(); 
                
                if(currency != "USD" && currency != "EUR"&& currency != "RUR"){
                        $("#provider_depo").val("");
                        my_alert("Неправильная валюта");       
                        return false;
                }
                if(amnt<10){
                        $("#provider_depo").val("");
                        my_alert("Ограничение минимальной суммы пополнения через OkPay");       
                        return false;
                }          
                
                var Res = $.ajax({
                                        url : "/finance/okpay/start/"+currency+"/"+amnt,
                                        type : 'GET',
                                        dataType: "json",
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider").html( "permission denied" );      
                                                $("#provider_depo").val("");
                                                return  false;
                                        },      
                                        success : function(Data){
                                                   if(Data["order_id"]){    
                                                        //$("#p_public_key").val(Data["public_key"]);         
                                                        $("#ok_invoice").val(Data["order_id"]);         
                                                        $("#o_amnt").val(Data["amount"]);                                                                 
                                                        $("#o_currency").val(Data["currency"]);         
                                                        $("#ok_return_success").val(Data["result_url"]);
                                                        $("#ok_return_fail").val(Data["result_url"]);         
                                                        $("#ok_ipn").val(Data["server_url"]);
                                                        finance.o_flag = true;
                                                        $("#pay_form").submit();                                            
                                                   }
                                         }
                                     });        
                
                
        },
        
        
        p_transfer: function(obj, Amnt, currency){
                if(currency != "USD" && currency != "EUR"){
                        obj.value = "";
                        my_alert("Неправильная валюта");       
                        return false;
                }
                if(Amnt<10){
                        obj.value = "";
                        my_alert("Ограничение минимальной суммы пополнения через PerfectMoney");       
                        return false;
                }          
                var Res = $.ajax({
                                        url : "/finance/perfectmoney/deposit/"+currency+"/"+Amnt,
                                        type : 'GET',
                                        cache: false,
                                        error: function(data){
                                                $("#res_provider").html( "permission denied" );      
                                                obj.value = "";
                                        },      
                                        success : function(Data){
                                                   var comission = ""; //"<p class=\"help-block\">Комиссия за пополнение составляет 2% с карты ПриватБанка, 2% + 10 грн с карт других банков</p>";
                                                    $("#res_provider").html( comission + Data ); 
                                                    $("#perfect_submit_button").css("margin-right","11em");
                                                    $("#perfect_submit_button").attr("class","btn btn-success pull-right");
                                                    $("#pay_p_form").bind( "submit", function() {
                                                         return finance.p_flag;
                                                         //strange but not work without it
                                                    });
                                                   $("#perfect_submit_button").bind( "click", finance.p_start);
                                                   
                                         }
                                     });   
                
        },
        p_start:function(){
                var currency = $("#currency_depo").val();
                var amnt = $("#amnt_depo").val(); 
                
                if(currency != "USD" && currency != "EUR"){
                        $("#provider_depo").val("");
                        my_alert("Неправильная валюта");       
                        return false;
                }
                if(amnt<10){
                        $("#provider_depo").val("");
                        my_alert("Ограничение минимальной суммы пополнения через PerfectMoney");       
                        return false;
                }          
                
                var Res = $.ajax({
                                        url : "/finance/perfectmoney/start/"+currency+"/"+amnt,
                                        type : 'GET',
                                        dataType: "json",
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider").html( "permission denied" );      
                                                $("#provider_depo").val("");
                                                return  false;
                                        },      
                                        success : function(Data){
                                                   if(Data["order_id"]){    
                                                        //$("#p_public_key").val(Data["public_key"]);         
                                                        $("#p_order_id").val(Data["order_id"]);         
                                                        $("#p_amt").val(Data["amount"]);                                                                 
                                                        $("#p_ccy").val(Data["currency"]);         
                                                        $("#p_return_url").val(Data["result_url"]);         
                                                        $("#p_server_url").val(Data["server_url"]);
                                                        $("#p_server_url_fail").val(Data["server_url_fail"]);         
                                                        finance.p_flag = true;
                                                        $("#pay_p_form").submit();                                            
                                                   }
                                         }
                                     });        
                
                
        },
        p24_start:function(){
                var currency = $("#currency_depo").val();
                var amnt = $("#amnt_depo").val(); 
                
                if(currency != "UAH"){
                        $("#provider_depo").val("");
                        my_alert("Неправильная валюта");       
                        return false;
                }
                if(amnt<100){
                        $("#provider_depo").val("");
                        my_alert("Ограничение минимальной суммы пополнения через Приват24, больше 100 ГРН");       
                        return false;
                }          
                
                var Res = $.ajax({
                                        url : "/finance/p24/start/"+amnt,
                                        type : 'GET',
                                        dataType: "json",
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider").html( "permission denied" );      
                                                $("#provider_depo").val("");
                                                return  false;
                                        },      
                                        success : function(Data){
                                                   if(Data["order_id"]){    
                                                        $("#p24_public_key").val(Data["public_key"]);         
                                                        $("#p24_order_id").val(Data["order_id"]);         
                                                        $("#p24_ext_details").val(Data["ext_details"]);         
                                                        $("#p24_amt").val(Data["amount"]);                                                                 
                                                        $("#p24_ccy").val(Data["currency"]);         
                                                        $("#p24_description").val(Data["description"]);         
                                                        $("#p24_return_url").val(Data["result_url"]);         
                                                        $("#p24_server_url").val(Data["server_url"]);         
                                                        $("#p24_type").val(Data["type"]);         
                                                        $("#p24_signature").val(Data["signature"]);         
                                                        finance.p24_flag = true;
                                                        $("#pay_p24_form").submit();                                            
                                                   }
                                         }
                                     });        
                
                
        },
        liqpay_start:function(){
                var currency = $("#currency_depo").val();
                var amnt = $("#amnt_depo").val(); 
                
                if(currency != "UAH"){
                        $("#provider_depo").val("");
                        my_alert("Неправильная валюта");       
                        return false;
                }
                if(amnt<100){
                        $("#provider_depo").val("");
                        my_alert("Ограничение минимальной суммы пополнения через liqpay, больше 100 ГРН");       
                        return false;
                }          
                
                var Res = $.ajax({
                                        url : "/finance/liqpay/start/"+amnt,
                                        type : 'GET',
                                        dataType: "json",
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider").html( "permission denied" );      
                                                $("#provider_depo").val("");
                                                return  false;
                                        },      
                                        success : function(Data){
                                                   if(Data["order_id"]){    
                                                        $("#liqpay_public_key").val(Data["public_key"]);         
                                                        $("#liqpay_order_id").val(Data["order_id"]);         
                                                        $("#liqpay_amount").val(Data["amount"]);         
                                                        $("#liqpay_currency").val(Data["currency"]);         
                                                        $("#liqpay_description").val(Data["description"]);         
                                                        $("#liqpay_result_url").val(Data["result_url"]);         
                                                        $("#liqpay_server_url").val(Data["server_url"]);         
                                                        $("#liqpay_type").val(Data["type"]);         
                                                        $("#liqpay_signature").val(Data["signature"]);         
                                                        $("#liqpay_language").val(Data["language"]);         
                                                        $("#liqpay_sandbox").val("1");                                                                

                                                        finance.liqpay_flag = true;
                                                        $("#pay_liqpay_form").submit();                                            
                                                   }
                                         }
                                     });               
                
        },
        p24_transfer: function(obj, Amnt, Currency){
                if(Currency != "UAH"){
                        obj.value = "";
                        my_alert("Неправильная валюта");       
                        return false;
                }
                if(Amnt<100){
                        obj.value = "";
                        my_alert("Ограничение минимальной суммы пополнения через Приват24, больше 100 ГРН");       
                        return false;
                }          
                var Res = $.ajax({
                                        url : "/finance/p24/deposit/"+Amnt,
                                        type : 'GET',
                                        cache: false,
                                        error: function(data){
                                                $("#res_provider").html( "permission denied" );      
                                                obj.value = "";
                                        },      
                                        success : function(Data){
                                                   var comission = "<p class=\"help-block\">Комиссия за пополнение составляет 2% с карты ПриватБанка, 2% + 10 грн с карт других банков</p>";
                                                    $("#res_provider").html( comission + Data );                                                  
                                                    $("#pay_p24_form").bind( "submit", function() {
                                                         return finance.p24_flag;
                                                         //strange but not work without it
                                                    });
                                                   $("#p24_submit_button").bind( "click", finance.p24_start);
                                                   
                                         }
                                     });   
                
        },
        liqpay_transfer: function(obj, Amnt, Currency){
                if(Currency != "UAH"){
                        obj.value = "";
                        my_alert("Неправильная валюта");       
                        return false;
                }
                if(Amnt<100){
                        obj.value = "";
                        my_alert("Ограничение минимальной суммы пополнения через liqpay, больше 100 ГРН");       
                        return false;
                }          
                var Res = $.ajax({
                                        url : "/finance/liqpay/deposit/"+Amnt,
                                        type : 'GET',
                                        cache: false,
                                        error: function(data){
                                                $("#res_provider").html( "permission denied" );      
                                                obj.value = "";
                                        },      
                                        success : function(Data){
                                                   var comission = "<p class=\"help-block\">Комиссия за пополнение составляет 2.75% с карт Visa, MasterCard</p>";
                                                   comission += "<p class=\"help-block\">1% наличными в терминалах ПриватБанка</p>"
                                                   $("#res_provider").html( comission + Data );                                                  
                                                    $("#pay_liqpay_form").bind( "submit", function() {
                                                         return finance.liqpay_flag;
                                                         //strange but not work without it
                                                    });
                                                   $("#liqpay_submit_button").bind( "click", finance.liqpay_start);
                                                   
                                         }
                                     });               
                
        },
        confirm_operation:function(){
                     var KeyType =   $("#key_type").val();
                     var Key =   $("#key").val();
                     var Pin =  $("#id_pin").val();
                     var params={ "key_type": KeyType, "pin": Pin};
                      $.ajax({
                                                url : "/finance/common_secure_confirm?key="+Key,
                                                type : 'POST', 
                                                data: params,
                                                error : function(Data){
                                                        my_alert("Авторизация не прошла");
                                                        
                                                },
                                                success : function(Data){
                                                         $("#home").html((Data));
                                                }
                             });  
                
                
        },
        confirm_g2a_operation:function(Session){
                     var KeyType =   $("#key_type").val()
                     var Key =   $("#key").val()
                     var params={"key_type": KeyType,"g2a_session": Session};
                      $.ajax({
                                                url : "/finance/common_secure_confirm?key="+Key,
                                                type : 'POST', 
                                                data: params,
                                                error : function(Data){
                                                        my_alert("Авторизация не прошла");
                                                        
                                                },
                                                success : function(Data){
                                                         $("#home").html((Data));
                                                }
                                        });  
                
                
        },
        bank_transfer: function(obj, Amnt, Currency){
                if(Currency != "UAH"){
                        obj.value = "";
                        my_alert("Неправильная валюта");       
                        return ;
                }
                if(Amnt<100){
                        obj.value = "";
                        my_alert("Ограничение минимальной суммы пополнения через банковские переводы, больше 100 ГРН");       
                        return ;
                }          
                var Res = $.ajax({
                                        url : "/finance/bank_transfer/UAH/" + Amnt,
                                        type : 'GET',
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider").html( "permission denied" );      
                                                obj.value = "";
                                        },      
                                        success : function(Data){
                                                   $("#res_provider").html( Data );                                             
                                         }
                                     });
                
                
                
        },        
        withdraw:function(Currency){
                $("#deposit_form").css({"display":"none"});
                window.scrollTo(0, 0);
                $("#res_provider_withdraw").html( "" );
                $("#currency_withdraw").val(Currency);
                $("#withdraw_form").slideDown("slow");
                finance.withdraw_providers(Currency);                
        },
        
         
        fill_usd_withdraw: function(){
                        $("#provider_withdraw").append( $('<option value="">Выбрать</option>') );
                        $("#provider_withdraw").append( $('<option value="perfect">Perfect Money</option>') );    
                        $("#provider_withdraw").append( $('<option value="okpay">OkPay</option>') );    
                        $("#label_provider_withdraw").html( "Cпособ вывода:" );                       
                        $("#provider_withdraw").show();
          
            
            
        },
        fill_eur_withdraw: function(){
                        $("#provider_withdraw").append( $('<option value="">Выбрать</option>') );
                        $("#provider_withdraw").append( $('<option value="perfect">Perfect Money</option>') );    
                        $("#provider_withdraw").append( $('<option value="okpay">OkPay</option>') );                    
                        $("#label_provider_withdraw").html( "Cпособ вывода:" );                       
                        $("#provider_withdraw").show();
        },
        fill_rur_withdraw: function(){
                        $("#provider_withdraw").append( $('<option value="">Выбрать</option>') );
                        $("#provider_withdraw").append( $('<option value="alfa">AlfaBank</option>') );    
                        $("#label_provider_withdraw").html( "Cпособ вывода:" );                       
                        $("#provider_withdraw").show();
        },
        
        withdraw_providers: function(Currency){
                $("#provider_withdraw").html("");                
                if(Currency == "UAH"){
                        
                        $("#provider_withdraw").show();
                        $("#label_provider_withdraw").show();
                        
                        $("#provider_withdraw").append( $('<option value="">Выбрать</option>') );
                  //      $("#provider_withdraw").append( $('<option value="bank_transfer">Банковский перевод</option>') );
                        //$("#provider_withdraw").append( $('<option value="liqpay_transfer">На счет LiqPay</option>') );    
                        $("#provider_withdraw").append( $('<option value="card_transfer">На платежную карту (Visa,MasterCard)</option>') );    

                }
                if(Currency == "USD"){
                    finance.fill_usd_withdraw();
                    return
                }
                if(Currency == "EUR"){
                    finance.fill_eur_withdraw();
                    return
                }
                if(Currency == "RUR"){
                    finance.fill_rur_withdraw();
                    return
                }
                
                
                if(finance.crypto_currency[Currency]){
                     
                        $("#provider_withdraw").hide();
                        $("#label_provider_withdraw").hide();
                        var Res = $.ajax({
                                        url : "/finance/crypto_transfer_withdraw/"+Currency,
                                        type : 'GET',
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider_withdraw").html( data );      
                                                
                                        },      
                                        success : function(Data){
                                                
                                                   $("#res_provider_withdraw").html( Data ); 
                                                   
                                        }
                                     });
                        
                        
                        
                        
                }
                
                
        },
        change_withdraw:function(obj){
                var provider = obj.value;
                if(provider == "")
                        return ;
                
                var currency = $("#currency_withdraw").val();                  
                if(provider == "bank_transfer")
                       return finance.bank_transfer_withdraw(obj,  currency )
                       
                if(provider == "liqpay_transfer")
                       return finance.liqpay_transfer_withdraw(obj,   currency )     
                
                if(provider == "card_transfer")
                       return finance.p2p_transfer_withdraw(obj,   currency )     
                       
                if(provider == "perfect")
                       return finance.perfect_transfer_withdraw(obj,  currency )
                       
                if(provider == "okpay")
                       return finance.okpay_transfer_withdraw(obj,   currency )     
                
                return
                       
                       
                       
                
                
        },
         perfect_transfer_withdraw:function(obj,  Currency){
                if(Currency != "USD" && Currency != "EUR" ){
                        obj.value = "";
                        my_alert("Неправильная валюта");       
                        return ;
                }
                var Amnt = 10;       
                var Res = $.ajax({
                                        url : "/finance/perfect_transfer_withdraw/"+Currency+"/" + Amnt,
                                        type : 'GET',
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider_withdraw").html( data );      
                                                obj.value = "";
                                        },      
                                        success : function(Data){
                                                   $("#res_provider_withdraw").html( Data ); 

                                         }
                                     });
                
                
        },
        okpay_transfer_withdraw:function(obj,  Currency){
                if(Currency != "USD" && Currency != "EUR" ){
                        obj.value = "";
                        my_alert("Неправильная валюта");       
                        return ;
                }
                var Amnt = 10;       
                var Res = $.ajax({
                                        url : "/finance/okpay_transfer_withdraw/"+Currency+"/" + Amnt,
                                        type : 'GET',
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider_withdraw").html( data );      
                                                obj.value = "";
                                        },      
                                        success : function(Data){
                                                   $("#res_provider_withdraw").html( Data ); 

                                         }
                                     });
                
                
        },
        
        
        p2p_transfer_withdraw:function(obj,  Currency){
                if(Currency != "UAH"){
                        obj.value = "";
                        my_alert("Неправильная валюта");       
                        return ;
                }
                var Amnt = 100;       
                var Res = $.ajax({
                                        url : "/finance/p2p_transfer_withdraw/"+Currency+"/" + Amnt,
                                        type : 'GET',
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider_withdraw").html( data );      
                                                obj.value = "";
                                        },      
                                        success : function(Data){
                                                   $("#res_provider_withdraw").html( Data ); 

                                         }
                                     });
                
                
        },
        bank_transfer_withdraw:function(obj,  Currency){
                if(Currency != "UAH"){
                        obj.value = "";
                        my_alert("Неправильная валюта");       
                        return ;
                }
                var Amnt =10;       
                var Res = $.ajax({
                                        url : "/finance/bank_transfer_withdraw/"+Currency+"/" + Amnt,
                                        type : 'GET',
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider_withdraw").html( data );      
                                                obj.value = "";
                                        },      
                                        success : function(Data){
                                                   $("#res_provider_withdraw").html( Data ); 

                                         }
                                     });
                
                
        },
        liqpay_transfer_withdraw:function(obj, Currency){
                if(Currency != "UAH"){
                        obj.value = "";
                        my_alert("Неправильная валюта");       
                        return ;
                }
                var Amnt = 10;
                var Res = $.ajax({
                                        url : "/finance/liqpay_transfer_withdraw/"+Currency+"/" + Amnt,
                                        type : 'GET',
                                        cache: false,
                                        error: function (data) {
                                                $("#res_provider_withdraw").html( data );      
                                                obj.value = "";
                                        },      
                                        success : function(Data){
                                                   $("#res_provider_withdraw").html( Data ); 

                                         }
                                     });
                
        }     
             
};
