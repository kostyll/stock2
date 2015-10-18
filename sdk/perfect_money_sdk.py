# -*- coding: utf-8 -*-

from crypton import settings

from base64 import b64encode
import hashlib 
from decimal import Decimal
from main.models import Accounts, TradePairs, Orders, Currency, TransError
from django.contrib.auth.models import User
import urllib2
import urllib
from django.http import HttpResponse 
import json
from xml.dom import minidom
from sdk.perfectmoney import PerfectMoney
enabled = False
if enabled:
    import sdk.perfect_money_settings

class perfect_money_sdk:
        
    @staticmethod          
    def str_class_name():
        return     "perfect_money"

    def get_traid_pair(self):
            return  self.__trade_pair

#public_key      
#private_key    
    
    
    def __init__(self,
                    Cur = "USD", 
                    public_id =  None,
                    password = None,
                    password2 = None,
            ):
        self.__public_id = public_id
        self.__password = password
        self.__password2 = password2
        self.__min_amnt = Decimal("1.00")
        self.comis = Decimal("0.00")
        self.description = "buying btc"
        PUser =  User.objects.get(username = perfect_money_sdk.str_class_name() )        
        CurrencyPay =  Currency.objects.get( title = Cur)        
        self.__currency = CurrencyPay
        self.__transit_account = Accounts.objects.get(user  = PUser, currency = CurrencyPay)
        self.__trade_pair = TradePairs.objects.get(transit_on = self.__transit_account,
                                                   transit_from  = self.__transit_account )
       
    
    def records(self, FromYear, FromMonth ):
          pass
    
    def generate_button(self, Amnt):
           acc = ""
	   currency = ""
           if self.__currency.title == "USD":
               acc=sdk.perfect_money_settings.USD
	       currency = "USD"
           elif self.__currency.title == perfect_money_sdk.str_class_name()+"_eur":
	       currency = "EUR"
               acc=sdk.perfect_money_settings.EUR
           elif self.__currency.title == "EUR":
	       currency = "EUR"
               acc=sdk.perfect_money_settings.EUR
           elif self.__currency.title == perfect_money_sdk.str_class_name()+"_usd":
	       currency = "USD"
               acc=sdk.perfect_money_settings.USD


           Data =  "<form id='pay_p_form' action=\"https://perfectmoney.is/api/step1.asp\" method=\"POST\">\
<p>\
    <input type=\"hidden\" id=\"p_public_key\" name=\"PAYEE_ACCOUNT\" value=\"%s\">\
    <input type=\"hidden\"  name=\"PAYEE_NAME\" value=\"BITCOIN TRADE COMPANY\">\
    <input type=\"hidden\" id=\"p_amt\" name=\"PAYMENT_AMOUNT\" value=\"%s\">\
    <input type=\"hidden\" id=\"p_ccy\" name=\"PAYMENT_UNITS\" value=\"%s\">\
    <input type=\"hidden\" id=\"p_server_url\" name=\"STATUS_URL\" \
        value=\"\">\
    <input type=\"hidden\"  id=\"p_return_url\" name=\"PAYMENT_URL\" \
        value=\"\">\
    <input type=\"hidden\" id=\"p_server_url_fail\" name=\"NOPAYMENT_URL\" \
        value=\"\">\
    <input type=\"hidden\" name=\"BAGGAGE_FIELDS\" \
        value=\"ORDER_NUM\">\
    <input type=\"hidden\" id=\"p_order_id\" name=\"ORDER_NUM\" value=\"\">\
    <input id='perfect_submit_button' type=\"submit\" name=\"PAYMENT_METHOD\" value=\"%s\" >\
</p>\
</form>" % (acc, Amnt, currency, u"Оплатить"  )
           return Data
       
    def   balance(self):
          pass
          
         

          
    def pay2p(self, OrderId, ToCard, Amnt):
          pass
          
#xml = """
#<?xml version="1.0" encoding="UTF-8"?> 
#<response version="1.0">
#<merchant>    <id>75482</id>  
#<signature>b253ad0eafd04aa50398c0b1617b18e5798f2330</signature>
#</merchant>
#<data>
#<oper>cmt</oper>  
#<payment id="" state="1" 
#message="" ref="aBESQ2509023364480" amt="1.0" 
#ccy="UAH" comis="3.0" code="" cardinfo="personified" /> 
#</data> </response>
#""".strip()          
          
    def generate_pay_request(self, User, Amount):
	currency = ""
        if self.__currency.title == "USD":
               currency = "USD"
        elif self.__currency.title == perfect_money_sdk.str_class_name()+"_eur":
               currency = "EUR"
        elif self.__currency.title == "EUR":
               currency = "EUR"
        elif self.__currency.title == perfect_money_sdk.str_class_name()+"_usd":
               currency = "USD"

        AmountStr = Decimal(Amount)    
        user_account = Accounts.objects.get(user  = User, currency = self.__currency)
        if AmountStr<0:
                raise TransError("NegativeAmount")
        
        if AmountStr < self.__min_amnt  :
                raise TransError("MinAmount")
        
        order = Orders(         user = User,
                                currency1 = self.__currency,
                                currency2 = self.__currency, 
                                price=AmountStr,
                                sum1_history = AmountStr,
                                sum2_history = AmountStr,
                                sum1 = AmountStr, 
                                sum2 = AmountStr,
                                transit_1 = self.__transit_account,
                                transit_2 = user_account,
                                trade_pair = self.__trade_pair,
                                status = "processing"
                        )
        order.save()
        ResultUrl = self.generate_result_url(order, User,  Amount )
        ServerResultUrl = self.generate_api_result_url(order, User,  Amount )
        
        Dict = {
                "public_key": self.__public_id,
                "order_id":   str(order.id),
                "result_url" : ResultUrl,
                "type":"perfectmoney",
                "ext_details":"none",
                "description" :self.description,
                "currency" :currency,
                "server_url": ServerResultUrl,
                "server_url_fail": self.generate_api_result_url_fail(order, User,  Amount ),
                "amount": "%.2f" % float(AmountStr)
                }
	
        Response =  HttpResponse( json.JSONEncoder().encode(Dict) )
        Response['Content-Type'] = 'application/json'
        return Response

    def generate_result_url(self, order, User,  Amount ):
            return settings.BASE_URL + "finance" #/" + str(order.id)
    
    def generate_api_result_url(self, order, User,  Amount ):
            return settings.BASE_URL + "finance/perfectmoney/hui_hui_hui/%s/%s" % ( self.__currency.title, str(order.id))
            
    def generate_api_result_url_fail(self, order, User,  Amount ):
            return settings.BASE_URL + "finance/perfectmoney/hui_hui_hui_hui/"+str(order.id)
    
    
    def check_payment(self, OrderId, verbose = False):
         pass
          
          
    def api_callback_pay(self, Params, callback):
               #<input type="hidden" name="PAYEE_ACCOUNT" value="U9007123">
    #<input type="hidden" name="PAYMENT_AMOUNT" value="109.99">
    #<input type="hidden" name="PAYMENT_UNITS" value="USD">
    #<input type="hidden" name="PAYMENT_BATCH_NUM" value="680">
    #<input type="hidden" name="PAYER_ACCOUNT" value="U110007">
    #<input type="hidden" name="TIMESTAMPGMT" value="1212244190">
    #<input type="hidden" name="ORDER_NUM" value="9801121">
    #<input type="hidden" name="CUST_NUM" value="2067609">
    #<input type="hidden" name="PAYMENT_ID" value="NULL">
    #<input type="hidden" 
          #name="V2_HASH" value="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX">
           perfectmoney = PerfectMoney(self.__public_id, self.__password)
             
            #def check(self, payee, payer, amount, units, batch_number, secret, timestamp, payment_id, v2_hash):
           if not perfectmoney.check(Params["PAYEE_ACCOUNT"],
                                     Params["PAYER_ACCOUNT"],
                                     float(Params["PAYMENT_AMOUNT"]),
                                     Params["PAYMENT_UNITS"],
                                     Params["PAYMENT_BATCH_NUM"],
                                     self.__password2,
                                     Params["TIMESTAMPGMT"],
                                     Params["PAYMENT_ID"],
                                     Params["V2_HASH"]
                                    ): 
                    raise TransError("Invalid Signature")
           callback(int(Params["ORDER_NUM"]), self.comis, self.__password)
           Response =  HttpResponse( json.JSONEncoder().encode({"status":True,"signature":True}) )
           Response['Content-Type'] = 'application/json'
           return Response

        




