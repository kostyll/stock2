"use strict";

var server_name = "bitcoin trade company";


var Main = {
        trade_pair:null,
        currency_base:"",
        currency_on:"",
        usd_uah_rate: null,
        timer_deals: null,
        chart: null,
        timer_sell_list: null,
        timer_buy_list: null,
        comission:0.0005, //0.1 percent
        start_last_price: function(){
                Main.last_price(function(){
                                setTimeout(Main.start_last_price, 5000)}
                                );
        
        },
        start_stock_stat:function(){
               Main.stock_stat(function(){
                               setTimeout(Main.start_stock_stat, 25000)}
               );
                
        },
        
        
        
        
        start_stock: function(){
               Main.start_deals_timer();
               Main.start_my_orders();
               Main.start_sell_list();
               Main.start_buy_list();
               Main.start_user_menu();
               //Main.start_market_prices();
               
               if(Main.currency_base == "UAH"){
                        $("#buy_result_usd_eq").show();
                        $("#sell_result_usd_eq").show();
                        $("#sell_price_usd_eq").show();                        
                        $("#buy_price_usd_eq").show();
                        
               }
               
             
               Main.draw_highcharts();
               
                
        },
        show_all_trade:function(){
                $("div.currency_pairs button.btn").removeClass("hidden");
          
            
            
        },
        start_time:function(){
                Main.server_time(function(){
                setTimeout(Main.start_time, 5000)});
                
        },
        val_eq_to_usd:function(Val, ResTo){
                if(Main.currency_base == "UAH"){
                      var Rate = Main.format_float4(Val/Main.usd_uah_rate);
                      $("#"+ResTo).html(Rate+"&nbsp;<strong>USD</strong>");                        
                        
               }               
        },
        eq_to_usd:function(obj, ResTo){
                if(Main.currency_base == "UAH"){
                      var Rate = Main.format_float4(obj.value/Main.usd_uah_rate);
                      $("#"+ResTo).html(Rate+"&nbsp;<strong>USD</strong>");                        
                        
               }               
        },
        server_time: function(callback){
                 $.ajax({
                              dataType: 'json',
                              url : "/time",
                              type : 'GET', 
                              cache: false,
                              error: function (data) {
                                                console.log(data);
                                                callback();
                              }, 
                              success : function(Data){
                                                Login.use_f2a = Data["use_f2a"];
                                                Login.sessionid = Data["sessionid"];
                                                Login.logged = Data["logged"];
                                                Main.usd_uah_rate = Data["usd_uah_rate"];
                                                $("#server_time").html( Data["time"] );
                                                $("#client_comis").html( Data["deal_comission"] );
                                                callback();
                                                
                                 }          
                              });     
                
        },
        stock_stat: function(callback){
                  if (!Main.trade_pair){
                     
                      Main.trade_pair='btc_usd';
                      Main.currency_base = "USD";
                      Main.currency_on = "BTC";
                                            
                  }
                     
                   $.ajax({
                              dataType: 'json',
                              url : "/api/day_stat/" + Main.trade_pair,
                              type : 'GET', 
                              cache: false,
                              error: function (data) {
                                                console.log(data);
                                                callback();
                              }, 
                              success : function(Data){
                                          $("#stock_min_price").html(Data["min"]+"&nbsp;"+Main.currency_base);
                                          $("#stock_max_price").html(Data["max"] +"&nbsp;"+Main.currency_base);
                                          var Volume = Data["volume_trade"]+"&nbsp;" + Main.currency_on + "&nbsp;/&nbsp;" + Data["volume_base"] + "&nbsp;" + Main.currency_base;
                                          $("#stock_volume").html(Volume);
                                          callback();
                               }
                              
                           });              
                
                
                
        },
        last_price: function(callback){
                  if (!Main.trade_pair){
                     
                      Main.trade_pair='btc_usd';
                      Main.currency_base = "USD";
                      Main.currency_on = "BTC";
                                            
                  }
                     
                   $.ajax({
                              dataType: 'json',
                              url : "/api/last_price/" + Main.trade_pair,
                              type : 'GET', 
                              cache: false,
                              error: function (data) {
                                                console.log(data);
                                                callback();
                              }, 
                              success : function(Data){
                                          $("#stock_last_price").html(Data["price"]+"&nbsp;"+Main.currency_base);
                                          callback();
                              }
                   });              

        },
        own_deals:function(callback){
                
                $.ajax({
                              dataType: 'json',
                              url : "/api/my_deals/" + Main.trade_pair,
                              type : 'GET', 
                              cache: false,
                              error: function (data) {
                                                console.log(data);
                        callback();
                              }, 
                              success : function(Data){
                                                var size = Data.length;
                                                $("#trade_deals").html("")   
                                                for(var i=0; i<size; i++){
                                                     var NewElement = "<tr>";
                                                     NewElement +="<td>" +Data[i]["pub_date"]+ "</td>";
                                                     NewElement +="<td><a href='/profile/"+Data[i]["user"]+"'>" +Data[i]["user"]+ "</a></td>";
                                                     if(Data[i]["type"] == "buy"){
                                                        NewElement +="<td style='color:green'>" +Data[i]["type"] + "</td>";
                                                     }else{
                                                        NewElement +="<td style='color:red'>" +Data[i]["type"] + "</td>";      
                                                     }
                                                     NewElement +="<td>" +Data[i]["price"]+ "&nbsp;<strong>" +Main.currency_base + "</strong></td>";
                                                     NewElement +="<td>" +Data[i]["amnt_base"] + "</td>";
                                                     NewElement +="<td>" +Data[i]["amnt_trade"] + "</td></tr>";                                                    
                                                     $("#trade_deals").append( NewElement );
                                                }
                        callback();
                                         }
                              });              
                
        },
        market_prices: function(callback){
                         $.ajax({
                             dataType: "json",
                             url : "/api/market_prices",
                             type : "GET", 
                             cache: false,
                             error: function (data) {
                                                console.log(data);
                        callback();
                             }, 
                             success : function(Data){
                                        var size = Data["prices"].length;
                                        var accounts = Data["prices"];
                                        for(var i=0; i<size; i++){
                                               var item = accounts[i];
                                               $("#" +  item["type"]).html( item["price"] );
                                        }
                    callback();
                                       
                                 }
                             }); 
                
        },
        user_menu: function(callback){
                         if(!Login.logged){
                setTimeout(callback, 23000);
                                return        
                         }
                
                         $.ajax({
                             dataType: "json",
                             url : "/api/balance",
                             type : "GET", 
                             cache: false,
                             error: function (data) {
                                                console.log(data);
                        setTimeout(callback, 23000);
                        return

                             }, 
                             success : function(Data){
                                        var size = Data["accounts"].length;
                                        var accounts = Data["accounts"];
                                        for(var i=0; i<size; i++){
                                               var item = accounts[i];
                                               $("#balance_" + item["currency"]).html( Main.format_float6(item["balance"]) );
                                        }
                                        Login.use_f2a = Data["use_f2a"];
                                        $("#notify_count").html("("+ Data["notify_count"] + ")");
                                        $("#msg_count").html("(" + Data["msg_count"] +")" );
                    callback();
                                 }
                             }); 
                 
                
        },
        create_msg: function(Whom){
                $("#msgs").hide();
                $("#msg_form").slideDown();
                $("#whom").val(Whom);
                        
        },
        send_msg: function(){
                        var params = {"whom":$("#whom").val(),"msg": $("#msg").val()  }
                        $.ajax({
                             url : "/msgs/create",
                             type : "POST", 
                             data : params,
                             cache: false,
                             error: function (data) {
                                                 my_alert(data);
                             }, 
                             success : function(Data){
                                       
                                        if(Data["status"]){
                                                window.location.href="/msgs/out";
                                                
                                        }else{
                                                my_alert(Data["description"]);
                                        }
                                     
                                     
                                }
                             
                                
                        }); 
                
                
                
        },
        cancel_msg:function(){
                $("#msgs").show("fast");
                $("#msg_form").hide("fast");
                $("#whom").val("");
                
        },
        notify_remove: function(id){
                
                         $.ajax({
                             dataType: "json",
                             url : "/msgs/hide/"+id,
                             type : "GET", 
                             cache: false,
                             error: function (data) {
                                                console.log(data);
                             }, 
                             success : function(Data){
                                        if(Data["status"]){
                                             $("#notify_"+id).hide();
                                             
                                        }else{
                                                my_alert("something wrong try later");
                                        }  
                                     
                                 }
                             }); 
                
        },
        start_market_prices: function(){

                console.log("market");
                Main.market_prices(   
            function(){
                        setTimeout(Main.start_market_prices, 5000);
            }   


        );
                
        },
        start_user_menu: function(){
        
                console.log("balance");
                Main.user_menu(function(){
                        setTimeout(Main.start_user_menu, 3000);
            }
        )
                
        },
        sell_list: function(callback){
                $.ajax({
                             dataType: "json",
                             url : "/api/trades/sell/" + Main.trade_pair,
                             type : "GET", 
                             cache: false,
                             error: function (data) {
                                                console.log(data);
                        callback();
                             }, 
                       
                             success : function(Data){
                                                        var size = Data["list"].length;
                                                        $("#sell_orders_list").html("");   
                                                        var List = Data["list"];
                                                        $("#sell_orders_sum").html( Data["orders_sum"] );
                                                        var MinPrice =Main.format_float6(Data["min_price"]);
                                                        $("#buy_min_price").html( MinPrice );
                                                        var min_price =   $("#buy_price").val(  );       
                                                        if(!min_price ){
                                                                    $("#buy_price").val( MinPrice );
                                                                    Main.val_eq_to_usd(MinPrice, "buy_price_usd_eq" );                                                                 
                                                        }
                                                        for(var i=0; i<size; i++){
                                                             
                                                                var usd_price =  Main.format_float4(List[i]["price"]/Main.usd_uah_rate);
                                                                var NewElement = "<tr class='cursor' onclick='Main.order2this_buy(this,"+ List[i]["price"] +","+ List[i]["currency_trade"] +" )'>";                                                        
                                                                NewElement +="<td>"  + Main.format_float6(List[i]["price"]) +"&nbsp;<strong>"  + Main.currency_base + "</strong>";
                                                                NewElement += "&nbsp;</td>";//<small>("+usd_price+"&#36;</small>)
                                                                NewElement +="<td >" + Main.format_float6(List[i]["currency_trade"]) + "</td>";
                                                                NewElement +="<td>"  + Main.format_float6(List[i]["currency_base"]) + "</td></tr>";
                                                                $("#sell_orders_list").append( NewElement );
                                                                
                                                        }                                                       
                                                        
                                                
                        callback();
                                         }
                             }); 
                
        },
        order2this_sell: function(obj, Price, Count){
                
             Price = Price*1-0.00000001;
             var Buy_count_id =   "#sell_count";
             var Buy_price_id =  "#sell_price"; 
             $(Buy_price_id).val(Price);
            
              if(Login.logged){
                var YourBalance = $("#balance_"+Main.currency_on).html();
                if(YourBalance>Count){
                        $(Buy_count_id).val(Count);
                }else{                     
                        $(Buy_count_id).val( YourBalance );
                }
                
              }else{
                $(Buy_count_id).val(Count);
              }
              Main.calc_order("sell");
             
                
        },
        order2this_buy: function(obj, Price, Count){
                
             Price = Price*1+0.00000001;
             var Buy_count_id =   "#buy_count";
             var Buy_price_id =  "#buy_price"; 
             $(Buy_price_id).val(Price);
            
              if(Login.logged){
                var YourBalance = $("#balance_"+Main.currency_base).html();
                if(YourBalance/Price>Count){
                        $(Buy_count_id).val(Count);
                }else{                     
                        $(Buy_count_id).val( Main.format_float8( YourBalance/Price ) );
                }
              }else{
                $(Buy_count_id).val(Count);
              }
              Main.calc_order("buy");
             
                
        },
        buy_list: function(callback){
                 $.ajax({
                              dataType: "json",
                              url : "/api/trades/buy/" + Main.trade_pair,
                              type : "GET", 
                              cache: false,
                              error: function (data) {
                                                console.log(data);
                        callback();
                              }, 
                              success : function(Data){
                                               
                                                        var size = Data["list"].length;
                                                        $("#buy_orders_list").html("");   
                                                        var List = Data["list"];
                                                        $("#buy_orders_sum").html( Data["orders_sum"] );
                                                        var MaxPrice = Main.format_float6(Data["max_price"]);
                                                        $("#sell_max_price").html( MaxPrice );
                                                        var max_price  = $("#sell_price").val()
                                                        if(!max_price ){
                                                                $("#sell_price").val( MaxPrice );
                                                                Main.val_eq_to_usd(MaxPrice, "sell_price_usd_eq");
                                                        }

                                                        for(var i=0; i<size; i++){
                                                                var usd_price =  Main.format_float4(List[i]["price"]/Main.usd_uah_rate);

                                                                var NewElement = "<tr class='cursor' onclick='Main.order2this_sell(this,"+ List[i]["price"] +","+ List[i]["currency_trade"] +" )'>";                                                        
                                                                NewElement +="<td>" + Main.format_float6(List[i]["price"]) +"&nbsp;<strong>" 
                                                                                 + Main.currency_base + "</td>";//</strong>&nbsp;<small>("+usd_price+"&#36;</small>)
                                                                NewElement +="<td>" +Main.format_float6( List[i]["currency_trade"]) + "</td>";
                                                                NewElement +="<td>" +Main.format_float6(List[i]["currency_base"]) + "</td></tr>";
                                                                $("#buy_orders_list").append( NewElement );
                                                        }
                        callback();
                                                
                                         }
                                     });            
          
                
        },    
        start_my_orders: function(){
               Main.my_orders(function(){
               console.log("call my orders");
               setTimeout(Main.start_my_orders, 5500);
           });
        },
        start_sell_list: function(){
                Main.sell_list(function(){
                console.log("sell list ");
                setTimeout(Main.start_sell_list, 3600);
        });
                
        },
        start_buy_list: function(){
                Main.buy_list(function(){
                console.log("buy list ");
                setTimeout(Main.start_buy_list, 3400);
        });
                
                
        },
        my_orders: function(callback){
                                if(!Login.logged){
                                        return callback();
                    
                                }
                                        
                                var Res = $.ajax({
                                        url : "/api/my_orders/" + Main.trade_pair,
                                        type : 'GET',
                                        dataType: 'json',
                                        cache: false,
                                        error: function (data) {
                                                console.log(data);
                        callback();
                                        },      
                                        success : function(Data){
                                                if(Data["auth"]){
                                                        var size = Data["your_open_orders"].length;
                                                        $("#your_open_orders").html("");   
                                                        var List = Data["your_open_orders"];
                                                        $("#your_balance_currency1").html(Data["balance_buy"]);
                                                        $("#your_balance_currency").html(Data["balance_sell"]);
                                                        for(var i=0; i<size; i++){
                                                                var NewElement = "<tr id=\"my_order_"+List[i]["id"]+"\"><td>"+List[i]["id"]+"</td>";
                                                                NewElement +="<td>" +List[i]["pub_date"] + "</td>";
                                                                NewElement +="<td>" +List[i]["type"] + "</td>";
                                                                NewElement +="<td>" +Main.format_float6(List[i]["price"]) +"&nbsp;<strong>" +Main.currency_base + "</strong></td>";
                                                                NewElement +="<td>" +Main.format_float6(List[i]["amnt_base"]) + "</td>";
                                                                NewElement +="<td>" +Main.format_float6(List[i]["amnt_trade"]) + "</td>";                                                    
                                                                NewElement +="<td> <span onclick=\"Main.remove('" + List[i]["id"] 
                                                                              +"')\" class=\"btn btn-primary btn-xs\">Cancel</span></td></tr>";                                                    
                                                                $("#your_open_orders").append( NewElement );
                                                        }
                                               }         
                                         callback();       
                                         }
                                     });

                        
                
        },
        remove: function(id){
                var call_id = "#my_order_"+id;
                $(call_id).hide();  
                $.ajax({
                                        dataType: 'json',
                                        url : "/api/remove/order/" + id,
                                        type : 'GET', 
                                        cache: false,
                                        error: function (data) {
                                             my_alert("Не могу удалить ордер  ");
                                             $(call_id).show();  
                                        }, 
                                        success : function(Data){
                                                if(Data["status"]){
                                                        $(call_id).hide();                                                     
                                                }else{
                                                        my_alert(Data["description"])
                                                        
                                                }
                                         }
                                     });      
                
        },
        deals_list: function(callback){
                
                                $.ajax({
                                        dataType: 'json',
                                        url : "/api/deals/" + Main.trade_pair,
                                        type : 'GET', 
                                        cache: false,
                                        error: function (data) {
                                                console.log(data);
                                                callback();
                                        }, 
                                        success : function(Data){
                                                var size = Data.length;
                                                $("#trade_deals").html("")   
                                                for(var i=0; i<size; i++){
                                                     var NewElement = "<tr>";
                                                     NewElement +="<td>" +Data[i]["pub_date"] + "</td>";
                                                     NewElement +="<td><a href='/profile/"+Data[i]["user"]+"'>" +Data[i]["user"]+ "</a></td>";
                                                     if(Data[i]["type"] == "buy"){
                                                        NewElement +="<td style='color:green'>" +Data[i]["type"] + "</td>";
                                                     }else{
                                                        NewElement +="<td style='color:red'>" +Data[i]["type"] + "</td>";      
                                                     }
                                                     
                                                     NewElement +="<td>" +Main.format_float4(Data[i]["price"]) +"&nbsp;<strong>" +Main.currency_base + "</strong></td>";
                                                     NewElement +="<td>" +Main.format_float4(Data[i]["amnt_base"]) + "</td>";
                                                     NewElement +="<td>" +Main.format_float4(Data[i]["amnt_trade"]) + "</td></tr>";                                                    
                                                     $("#trade_deals").append( NewElement );
                                                }
                                                callback();
                                         }
                                     });                                
                                
                                
        },
        start_deals_timer: function(){
                Main.deals_list(function(){
                console.log("deal list ");
                setTimeout(Main.start_deals_timer, 4500);
        });
        },
        make_order: function(Currency, Currency1){
                
                  var Price  =  $("#buy_price").val();
                  var Count  =  $("#buy_count").val();
                  var params = {"count":  Count, "price": Price , "currency1": Currency1, "currency": Currency }
                  $.ajax({
                        url : "/api/buy/" + Main.trade_pair,
                        type : 'POST', 
                        data: params,
                        dataType:'json',
                        success : function(data){
                                
                                if(data["status"] == true){
                                   my_alert(data["description"]);               
                                   $("#buy_count").val("0");
                                   $("#buy_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                                   return
                                }
                                
                                if(data["status"] == 'incifition_funds'){
                                     my_alert(data["description"]);   
                                     return 

                                }
                                if(data["status"] == 'processed'){
                                     my_alert(data["description"]);
                                     $("#buy_count").val("0");
                                     $("#buy_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                                     return 

                                        
                                }                    
                                if(data["status"] == 'part_processed'){
                                     my_alert(data["description"]);
                                     $("#buy_count").val("0");
                                     $("#buy_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                                     return
                                        
                                } 
                                my_alert("Не могу создать ордер, проверьте пожайлуста данный и попробуйте снова");
                                
                                
                                
                                
                        }
                        
                       });

                
                
        },
        make_order_sell:function(Currency, Currency1){
                  var Price  =  $("#sell_price").val();
                  var Count  =  $("#sell_count").val();
                  var params = {"count":  Count, "price": Price , "currency1": Currency1, "currency": Currency }
                  $.ajax({
                         url : "/api/sell/" + Main.trade_pair,
                         type: 'POST', 
                         data: params,
                         dataType:'json',
                         success : function(data){
                                if(data["status"] == true){
                                   my_alert(data["description"]);               
                                   $("#sell_count").val("0");
                                   $("#sell_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                                   return

                                }
                                
                                if(data["status"] == 'incifition_funds'){
                                     my_alert(data["description"]);   
                                     return

                                }
                                if(data["status"] == 'processed'){
                                     my_alert(data["description"]);
                                     $("#sell_count").val("0");
                                     $("#sell_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                                     return

                                        
                                }                    
                                if(data["status"] == 'part_processed'){
                                     my_alert(data["description"]);
                                     $("#sell_count").val("0");
                                     $("#sell_help").html("Нажмите посчитать, чтобы рассчитать сумму в соответствии с ордерами.");
                                     return

                                        
                                } 
//                                 my_alert("Не могу создать ордер, проверьте пожайлуста данный и попробуйте снова");

                                
                        }
                        
                       });
                
                
        },
        calc_order: function(Form){
                      var Buy_count_id =   "#"+Form +"_count";
                      var Buy_price_id =  "#" + Form +"_price";
                      var result_id =   "#" + Form +"_result";
                      var comission_id =  "#" +  Form +"_comission";
                      var comission_form = "#" + Form + "_comission_form"; 
                      var Count = $(Buy_count_id).val();
                      var PriceEach = $(Buy_price_id).val();
                      if(Count<Main.min_deal){
                              if( Form =="buy"){
                                        my_alert("К сожелению сумма сделки меньше минимальной возможной");
                              }else{
                                        my_alert("К сожелению сумма сделки меньше минимальной возможной");
                                      
                              }
                              return
                              
                      }
                      
                      //  console.log(Buy_count_id + " " + Count + " " + Buy_price_id + " " +PriceEach );
                      var WholeSum = PriceEach * Count ;
//                       var ComissionSum = ( PriceEach * Count) * Main.comission;
                      $(result_id).html( Main.format_float8( WholeSum ) );
                      Main.val_eq_to_usd(WholeSum, Form+"_result_usd_eq");
                      
                      if( Form =="buy"){
                            var ComissionSumTorg = Count * Main.comission ;                
                            $(comission_id).html( Main.format_float8( ComissionSumTorg ) ) ;     
                            $(comission_form).show();
//                             $("#buy_help").html("Вы получаете  " +
//                                                 Main.format_float8( Count - ComissionSumTorg  ) + " " +
//                                                 Main.currency_on
//                                                )
                      }else{
                            var ComissionSumTorg = WholeSum * Main.comission ;                
                            $(comission_id).html( Main.format_float8( ComissionSumTorg ) ) ;     
                            $(comission_form).show(); 
//                             $("#sell_help").html("Вы получаете  " +
//                                                 Main.format_float8(WholeSum - ComissionSumTorg  ) + " " +
//                                                 Main.currency_base
//                                                )
                      }
                
        },
        calc_straight:function(obj){
                   var Funds = obj.innerHTML;
                   $("#sell_count").val(Funds);                    
        },
        calc_over:function(obj){
                   var Funds = obj.innerHTML;
                   console.log("calculate " + Funds);
                   var min_price = $("#buy_price").val();                   
                   
                   $("#buy_count").val(Main.format_float8(Funds/min_price));

                   
        },
        format_float6 : function(Val){
        if(Val<0.001)
            return Main.format_float8(Val)
                var NewVal = Val*1000000;
                return Math.floor(NewVal)/1000000;
                
        },
        format_float4 : function(Val){
                if(Val<0.01)
            return Main.format_float6(Val)
        var NewVal = Val*1000;
                return Math.floor(NewVal)/1000;
                
        },
        format_float8 : function(Val){
        if(Val<0.00001)
            return Main.format_float12(Val);
                var NewVal = Val*1000000;
                return Math.floor(NewVal)/1000000;
                
        },
        format_float12 : function(Val){
                return Val;
        var NewVal = Val*10000000000;
                return Math.floor(NewVal)/10000000000+'';
                
        },
        drawVisualization:function(){
              var Width =  screen.width;
                
              var WidthAdapting ={
                1280: 800,
                1600: 945,
                1360: 800,
                1920: 1038

               };
               var working_width = WidthAdapting[Width];
               if(!working_width){
                        working_width = 800;
                }
                
                $.ajax({
                         url : "/api/japan_stat/" + Main.trade_pair,
                         type: 'GET', 
                         dataType:'json',
                         success : function(Data){
                                                console.log(Data["trades"]);
                                                var data = google.visualization.arrayToDataTable(Data["trades"], true);
                                                $("#online_users").html(Data["online"]);
                                                $("#volume_base").html(Data["volume_base"]);
                                                $("#volume_trade").html(Data["volume_trade"]);
                                               
                                                var options = {
                                                legend:'none',
                                                width:working_width,
                                                height:250,
                                                fontSize:10,
                                                chartArea: {
//                                                         left:40,
//                                                         top:40,
                                                       width:working_width-200,
                                                        height:150
                                                        },
                                                colors:["#515151","#515151"],
                                                candlestick:{
                                                                        fallingColor:{
                                                                        fill: "#0ab92b",
                                                                       stroke: "green",
                                                                        strokeWidth: 1
                                                                },
                                                                risingColor:{
                                                                        fill: "#f01717",
                                                                        stroke: "#d91e1e",
                                                                        strokeWidth: 1
                                                                },
                                                                hollowIsRising: true
                                        },
                                        hAxis :{maxValue: 100},
                                        series: {0: {type: "candlesticks"}, 
                                                1: {type: "bars", targetAxisIndex:1, color:"#ebebeb"} },
                                        
                                        };
                        var chart = new google.visualization.CandlestickChart(document.getElementById('chart_trade'));
                        chart.draw(data, options);
         
                     }
         
        });
        
               
    },
    draw_highcharts:function(){
                var Width =  screen.width;
                
                var WidthAdapting ={
                };
                
                var working_width = WidthAdapting[Width];
                console.log("screen with" + Width)
                working_width = 812 ;//  Width*0.6391;
                //         }
                // }
                $("#chart_trade").css({width:working_width});
            
                $.ajax({
                         url : "/api/japan_stat/high/" + Main.trade_pair,
                         type: 'GET', 
                         dataType:'json',
                         success : highchart_candle
                });

                // split
                        
            
            
        
            
    },
    highcharts_thema_enable:function(){
                if(Main.highcharts_enabled)
                        return true;

                Highcharts.createElement('link', {
                href: 'https://fonts.googleapis.com/css?family=Signika:400,700',
                rel: 'stylesheet',
                type: 'text/css'
                }, null, document.getElementsByTagName('head')[0]);

                // Add the background image to the container
                Highcharts.wrap(Highcharts.Chart.prototype, 'getContainer', function (proceed) {
                proceed.call(this);
           //     this.container.style.background = 'url(https:///img/sand.png)';
                });


                Highcharts.theme = {
                colors: ["gray", "#8085e9", "#8d4654", "#7798BF", "#aaeeee", "#ff0066", "#eeaaee",
                         "#55BF3B", "#DF5353", "#7798BF", "#aaeeee"],
                chart: {
                backgroundColor: null,
                style: {
                        fontFamily: "Signika, serif"
                }
                },
                title: {
                style: {
                        color: 'black',
                        fontSize: '16px',
                        fontWeight: 'bold'
                }
                },
                subtitle: {
                style: {
                        color: 'black'
                }
                },
                tooltip: {
                borderWidth: 0
                },
                legend: {
                itemStyle: {
                        fontWeight: 'bold',
                        fontSize: '13px'
                }
                },
                xAxis: {
                labels: {
                        style: {
                        color: '#6e6e70'
                        }
                }
                },
                yAxis: {
                labels: {
                        style: {
                        color: '#6e6e70'
                        }
                }
                },
                plotOptions: {
                series: {
                        shadow: true
                },
                candlestick: {
                        lineColor: '#404048',
                        color: '#f01717',
                        upColor: '#43ac6a'
                },
                map: {
                        shadow: false
                }
                },

                // Highstock specific
                navigator: {
                xAxis: {
                        gridLineColor: '#D0D0D8'
                }
                },
                rangeSelector: {
                buttonTheme: {
                        fill: 'white',
                        stroke: '#C0C0C8',
                        'stroke-width': 1,
                        states: {
                        select: {
                        fill: '#D0D0D8'
                        }
                        }
                }
                },
                scrollbar: {
                trackBorderColor: '#C0C0C8'
                },

                // General
                background2: '#E0E0E8'
                
                };
                Highcharts.setOptions(Highcharts.theme);
                Highcharts.setOptions({
                                        global : {
                                                useUTC : false
                                        },
                                        lang: {
                                                loading: 'Загружаем',
                                                months: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июдь', 'Авгут',
                                                'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
                                                weekdays: ['Воскресенье','Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятьница', 'Суббота'],
                                                shortMonths: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июль', 'Авг', 'Сент', 
                                                                'Окт', 'Ноя', 'Дек'],
                                                exportButtonTitle: "Экспортировать",
                                                printButtonTitle: "Печать",
                                                rangeSelectorFrom: "С",
                                                rangeSelectorTo: "По",
                                                rangeSelectorZoom: "Период",
                                                downloadPNG: 'Скачать в  PNG',
                                                downloadJPEG: 'Скачать в  JPEG',
                                                downloadPDF: 'Скачать PDF',
                                                downloadSVG: 'Скачать SVG'
                                                // resetZoom: "Reset",
                                                // resetZoomTitle: "Reset,
                                                // thousandsSep: ".",
                                                // decimalPoint: ','
                                }
                                }
                                );
                        Main.highcharts_enabled =  true;

                        
        },
        confirm_operation_privatkey:function(){
                     var KeyType =   $("#key_type").val()
                     var Key =   $("#key").val()
                     var Pin =  $("#id_pin").val()
                     var params={"key": Key, "key_type": KeyType, "pin": Pin};
                      $.ajax({
                                                url : "/profile/private_key",
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
        confirm_g2a_privatkey:function(Session){
                     var KeyType =   $("#key_type").val()
                     var Key =   $("#key").val()
                     var params={"key": Key, "key_type": KeyType,"g2a_session": Session};
                      $.ajax({
                                                url : "/profile/private_key",
                                                type : 'POST', 
                                                data: params,
                                                error : function(Data){
                                                        my_alert("Авторизация не прошла");
                                                        
                                                },
                                                success : function(Data){
                                                         $("#home").html((Data));
                                                }
                                        });  
                
                
        }
}
var Stock  = {
        current_index:null,
        btce_serias_ask:null,
        btce_serias_bid:null,
        btce_serias_vol:null,        
        sel_button: null,
        foreign_stock_name:null,
        foreign_stock: function(type, my_stock, obj){
                if(type == "btc_e" && my_stock =="btc_uah"){
                    $('#chart_trade').highcharts().destroy();
                    $("#stocks_trades .current_stock").removeClass("btn-success").removeClass("current_stock").addClass("btn-default");
                    $(obj).addClass("btn-success").addClass("current_stock");
                    Stock.draw_btce_stock("btc_usd");
                    return   
                }
                if(type == "btc_e" && my_stock =="ltc_uah"){
                    $('#chart_trade').highcharts().destroy();
                    $("#stocks_trades .current_stock").removeClass("btn-success").removeClass("current_stock").addClass("btn-default");
                    $(obj).addClass("btn-success").addClass("current_stock");
                    Stock.draw_btce_stock("ltc_usd");
                    return   
                }
                if(type == "btc_e" && my_stock =="nvc_uah"){
                    $('#chart_trade').highcharts().destroy();
                    $("#stocks_trades .current_stock").removeClass("btn-success").removeClass("current_stock").addClass("btn-default");
                    $(obj).addClass("btn-success").addClass("current_stock");
                    Stock.draw_btce_stock("nvc_usd");
                    return   
                }
                
                
                
                my_alert("Еще немного и будет сделано, терпение");
                        
                
               
        },
        own: function(obj){
                    $('#chart_trade').highcharts().destroy();
                    $("#stocks_trades .current_stock").removeClass("btn-success").removeClass("current_stock").addClass("btn-default");
                    $(obj).removeClass("btn-default").addClass("btn-success").addClass("current_stock");
                    Main.draw_highcharts();
                
        },
        draw_btce_stock:function(StockType){
          
           Stock.foreign_stock_name = StockType;     
           $.ajax({
              url : "/foreign/stock/btce/"+StockType+"/minute/0",
              type: 'GET', 
              dataType:'json',
              success: draw_btce_stock
              });     
             
                
        },
         
        update_btce_stock:function(){         
              console.log(Stock.foreign_stock_name);
              $.ajax({
              url : "/foreign/stock/btce/"+ Stock.foreign_stock_name+"/minute/"+Stock.current_index,
              type: 'GET', 
              dataType:'json',
              success: function(Data){
                   Stock.current_index = Data["last"];
                   console.log(Stock.current_index);
                   var array = Data["data_ask"];
                   for(var i=0;i<array.length;i++ ){
                           Stock.btce_serias_ask.addPoint([ array[i][0], array[i][1] ], true, true);
                   }
                   array = Data["data_bid"];
                   for(var i=0;i<array.length;i++ ){
                           Stock.btce_serias_bid.addPoint([ array[i][0], array[i][1] ], true, true);
                   }
                   array = Data["data_vol"];
                   for(var i=0;i<array.length;i++ ){
                           Stock.btce_serias_vol.addPoint([ array[i][0], array[i][1] ], true, true);
                   }
               
              }
              });
       }
        
        
        
}
function draw_btce_stock(Data){
                        Stock.current_index = Data["last"];
                        
                        $('#chart_trade').highcharts('StockChart', {
                        chart : {
                                events : {
                                        load : function() {
                                              Stock.btce_serias_ask = this.series[0];
                                              Stock.btce_serias_bid = this.series[1];
                                              Stock.btce_serias_vol = this.series[2];
                                              setInterval(Stock.update_btce_stock, 5000);                                   
                                        }
                                }
                        },
                        rangeSelector: {
                                buttons: [ {
                                        count: 1,
                                        type: 'day',
                                        text: '1d'
                                }, 
                                {
                                        count: 5,
                                        type: 'day',
                                        text: '5d'
                                }, {
                                        type: 'all',
                                        text: 'All'
                                }],
                                inputEnabled: false,
                                selected: 0
                        },
                        
                        title : {
                                text : 'Торги BTC-e  Биткоин к USD'
                        },
                        
                        exporting: {
                                enabled: false
                        },
                        yAxis: [{
                        labels: {
                                align: 'right',
                                x: -3
                        },
                        title: {
                            text: 'Продажа'
                        },
                        height: '60%',
                        plotOptions: {
                                series: {
                                        compare: 'percent'
                                }
                        },
                         tooltip: {
                                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                                valueDecimals: 2
                        },
                        lineWidth: 2
                        }, 
                        {
                        labels: {
                                align: 'right',
                                x: -3
                        },
                        title: {
                            text: 'Покупка'
                        },
                        plotOptions: {
                                series: {
                                        compare: 'percent'
                                }
                        },
                        tooltip: {
                                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                                valueDecimals: 2
                        },
                        height: '60%',
                        lineWidth: 2
                        }, 
                        
                        {
                        labels: {
                                align: 'right',
                                x: -3
                        },
                        title: {
                            text: 'Volume'
                        },
                        top: '65%',
                        height: '35%',
                        offset: 0,
                        lineWidth: 2
                        
                                
                        },
                                
                        
                        ],
                        
                        series : [
                        
                       
                        {
                                name : 'Продажа',
                                data : Data["data_ask"]
                        },
                        {
                                name : 'Покупка',
                                data : Data["data_bid"]
                        },
                        {
                                type: "column",
                                name : 'Объем',
                                yAxis: 2,
                                data : Data["data_vol"]
                        }
                        
                        
                        ]
                   });
                
        }




function highchart_candle(Data){
// split the data set into ohlc and volume
                Main.highcharts_thema_enable();
                $("#online_users").html(Data["online"]);
                $("#volume_base").html(Data["volume_base"]);
                $("#volume_trade").html(Data["volume_trade"]);
                var data = Data["trades"];
      
                Highcharts.setOptions(Highcharts.theme);
                var ohlc = [],volume = [],dataLength = data.length;                        
                for (var i = 0; i < dataLength; i++) {
                        ohlc.push([
                                data[i][0], // the date
                                data[i][1], // open
                                data[i][2], // high
                                data[i][3], // low
                                data[i][4] // close
                
                
                        ]);
                        
                        volume.push([
                                data[i][0], // the date
                                data[i][5] // the volume
                        ])
                }

                // set the allowed units for data grouping
                var groupingUnits = [[
                        'week',                         // unit name
                        [1]                             // allowed multiples
                ], [
                        'month',
                        [1, 2, 3, 4, 6]
                ]];    
                // create the chart
                $('#chart_trade').highcharts('StockChart', {
                    
                     rangeSelector: {
                         buttons:
                         [
                         {
                                type: 'day',
                                count: 1,
                                text: '1d'
                         },
                          {
                                type: 'week',
                                count: 1,
                                text: '1w'
                         },
                         {
                                type: 'month',
                                count: 1,
                                text: '1m'
                        }, 
                        {
                                type: 'month',
                                count: 3,
                                text: '3m'
                        }, {
                                type: 'month',
                                count: 6,
                                text: '6m'
                        },
                        {
                                type: 'year',
                                count: 1,
                                text: '1y'
                        }
                                 
                        ],    
                         inputEnabled: $('#chart_trade').width() > 480,
                         selected: 4
                     },
        
            
                    title: {
                        text: ''//'Торги'
                    },

                    yAxis: [{
                        labels: {
                                align: 'right',
                                x: -3
                        },
                        title: {
                            text: 'Котировки'
                        },
                        height: '60%',
                        lineWidth: 2
                    }, {
                        labels: {
                                align: 'right',
                                x: -3
                        },
                        title: {
                            text: 'Объем'
                        },
                        top: '65%',
                        height: '35%',
                        offset: 0,
                        lineWidth: 2
                    }],
                    
                    series: [{
                        type: 'candlestick',
                        name: 'Торги',
                        data: ohlc,
                        dataGrouping: {
                                        enable: false 
                    //units: groupingUnits
                        }
                     }, {
                        type: 'column',
                        name: 'Объем',
                        data: volume,
                        yAxis: 1,
                        dataGrouping: {
                                    enable:false
                   //units: groupingUnits
                        }
                    }]
                });
}




function hide_modal(id){
        $('#'+id).modal('hide'); 
}

function my_alert(Msg){
         $('#modal_msg').html(Msg);                // initializes and invokes show immediately
         $('#modal_dlg').modal('show');               // initializes and invokes show immediately
          
        
}


