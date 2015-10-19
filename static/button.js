"use strict";
var btc_trade_ua_button = {
        host:"https://btc-trade.com.ua",
        getHttp: function(){
                        var req=null;
                        if(window.XMLHttpRequest){

                                req=new XMLHttpRequest();
                                return req;
                        }else if (window.ActiveXObject)
                        {
                                req=new XDomainRequest();

                                //ActiveXObject("Microsoft.XMLHTTP");
                                return req;
                        }else{
                                alert("sorry,change you browser please");
                                return req;
                        }


        },
        start:function( ID, Type ){
              var xmlhttp = btc_trade_ua_button.getHttp();
              xmlhttp.onreadystatechange=function()
              {
                        if (xmlhttp.readyState==4 && xmlhttp.status==200)
                        {
                                document.getElementById(ID).innerHTML = xmlhttp.responseText;
                        }
              };
              xmlhttp.open("GET",btc_trade_ua_button.host + "/project/banner/"+Type+"?_=123",true);
              xmlhttp.send();                
        }
};

btc_trade_ua_button.start("btc_trade_ua_button_div1", "one");
btc_trade_ua_button.start("btc_trade_ua_button_div2", "two");
btc_trade_ua_button.start("btc_trade_ua_button_div3", "three");
