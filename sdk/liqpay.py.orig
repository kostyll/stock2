# -*- coding: utf-8 -*-

from crypton import settings

from base64 import b64encode
import hashlib 
from decimal import Decimal
from main.api import TransError
from main.api import add_trans
from main.msgs import notify_email
from main.models import Accounts, TradePairs, Orders, Trans, Currency, LiqPayTrans
from django.contrib.auth.models import User
from django.http import HttpResponse 
import json

###TODO remove HTTP RESPONSE
class liqpay:
        
    @staticmethod          
    def str_class_name():
        return     "liqpay"

    def get_traid_pair(self):
            return  self.__trade_pair

#public_key      
#private_key     
    
    def __init__(self,  lang = "ru", Cur = "UAH" ,settings_file = ""):
     
        self.__public_key = settings.LIQPAY_MERCHID
        self.__private_key = settings.LIQPAY_KEY
        self.__my_orderid_key = "heheheh"
        self.__type = "buy"
        self.__min_amnt = Decimal("100.00")
        self.__comis = Decimal("0.01")
        self.__language = lang
        self.__description = "BTC TRADE UA, buying BTC, information service payments"
        LiqPayUser =  User.objects.get(username = liqpay.str_class_name() )        
        CurrencyPay =  Currency.objects.get( title = Cur)        
        self.__currency = CurrencyPay
        self.__transit_account = Accounts.objects.get(user  = LiqPayUser, currency = CurrencyPay)
        self.__trade_pair = TradePairs.objects.get(transit_on = self.__transit_account,
                                                   transit_from  = self.__transit_account )
        
    def  generate_button(self, Amnt):
        return    "<form   id=\"pay_liqpay_form\" method=\"POST\" action=\"https://www.liqpay.com/api/pay\" accept-charset=\"utf-8\">\
                        <input type=\"hidden\" id=\"liqpay_public_key\" name=\"public_key\" value=\"%s\" />\
                        <input type=\"hidden\" id=\"liqpay_amount\" name=\"amount\" value=\"%s\" />\
                        <input type=\"hidden\" id=\"liqpay_currency\" name=\"currency\" value=\"%s\" />\
                        <input type=\"hidden\" id=\"liqpay_description\" name=\"description\" value=\"%s\" />\
                        <input type=\"hidden\" id=\"liqpay_order_id\" name=\"order_id\" value=\"\" />\
                        <input type=\"hidden\" id=\"liqpay_result_url\" name=\"result_url\" />\
                        <input type=\"hidden\" id=\"liqpay_server_url\" name=\"server_url\"  />\
                        <input type=\"hidden\" id=\"liqpay_type\" name=\"type\" value=\"buy\" />\
                        <input type=\"hidden\" id=\"liqpay_signature\" name=\"signature\" value=\"\" />\
                        <input type=\"hidden\" id=\"liqpay_language\" name=\"language\" value=\"%s\" />\
                        <input id=\"liqpay_submit_button\" type=\"image\" src=\"https://static.liqpay.com/buttons/p1ru.radius.png\" \
                        name=\"btn_text\" />\
                </form>"  % (self.__public_key, str(Amnt),self.__currency, self.__description, self.__language )
                

#<input type=\"hidden\" id=\"liqpay_sandbox\" name=\"sandbox\" value=\"0\" />\

        
###TODO remove HTTP RESPONSE
   
    def generate_pay_request(self, User, Amount):
        AmountStr = Decimal(Amount)    
        user_account = Accounts.objects.get(user  = User, currency = self.__currency)
        if AmountStr<0:
                raise TransError("NegativeAmount")
        if AmountStr<self.__min_amnt:
                raise TransError("MinAmount")
        order = Orders(         user = User,
                                currency1 = self.__currency,
                                currency2 = self.__currency, 
                                sum1_history = AmountStr,
                                sum2_history = AmountStr,
                                sum1 = AmountStr, 
                                sum2 = AmountStr,
                                transit_1 = self.__transit_account,
                                transit_2 = user_account,
                                trade_pair = self.__trade_pair,
                                status = "created"
                        )
        order.save()
        ResultUrl = self.generate_result_url(order, User,  Amount )
        ServerResultUrl = self.generate_api_result_url(order, User,  Amount )
        m = hashlib.sha1(self.__private_key + 
                         str(AmountStr) +
                         self.__currency.title  +
                         self.__public_key +
                         str(order.id) +
                         self.__type +
                         self.__description +
                         ResultUrl +
                         ServerResultUrl
                         )
        signature = b64encode( m.digest() )
        Dict = {
                "signature":signature,
                "public_key": self.__public_key,
                "order_id":   str(order.id),
                "result_url" : ResultUrl,
                "language" : self.__language,
                "type" : self.__type,
                "description" :self.__description,
                "currency" :self.__currency.title,
                "server_url": ServerResultUrl,
                "amount": str(AmountStr)
                }
        Response =  HttpResponse( json.JSONEncoder().encode(Dict) )
        Response['Content-Type'] = 'application/json'
        return Response  

    def generate_result_url(self, order, User,  Amount ):
            return settings.BASE_URL + "finance/common_confirm_page/" + str(order.id)
    
    def generate_api_result_url(self, order, User,  Amount ):
            return settings.BASE_URL + "finance/liqpay/hui_hui_hui/"+str(order.id)
    
    def api_callback_pay(self, Params):
           PublicKey = Params["public_key"] 
           Amount =  Params["amount"] 
           CurrencyStr = Params["currency"] 
           Desc = Params["description"]
           Type = Params["type"]
           OrderId = Params["order_id"]
           Status = Params["status"]
           OutOrderId = Params["transaction_id"]
           Phone = Params["sender_phone"]
           Signature = Params["signature"]
           Comission = Decimal(Params["receiver_commission"])
           m = hashlib.sha1(self.__private_key + 
                         Amount +
                         CurrencyStr  +
                         self.__public_key +
                         OrderId +
                         self.__type +
                         self.__description +
                         Status +
                         OutOrderId +
                         Phone
                         )
           
           signature = b64encode( m.digest() )       
           if signature != Signature: 
                    raise TransError("Invalid Signature")
             
           if Status == "failure":
                     order = Orders.objects.get( id = int(OrderId) )
                     order.status = "order_cancel"
                     order.save()
                     Response =  HttpResponse( json.JSONEncoder().encode({"status":True,"signature":True}) )
                     Response['Content-Type'] = 'application/json'
                     return Response
             
           if Status == "wait_secure":
                     order = Orders.objects.get( id = int(OrderId), status="created" )
                     order.status = "wait_secure"
                     order.save()
                     Response =  HttpResponse( json.JSONEncoder().encode({"status":True,"signature":True}) )
                     Response['Content-Type'] = 'application/json'
                     return Response
           ##TODO add system message  
           if Status == "success":
                     order = Orders.objects.get(id = int(OrderId) )
                     if order.status !="created" and order.status !="wait_secure":
                             raise TransError("Invalid order")
                     order.status="processing"
                     order.save()
 		     from main.models import check_holds
                     check_holds(order)
                     add_trans( order.transit_1 , order.sum1, self.__currency,
                                order.transit_2, order, 
                                "payin", OutOrderId, False)
                     
                     #hack if privat is wrong  
                     HackComis = order.sum1 * self.__comis
		     if Comission < HackComis:
			Comission = HackComis

                     add_trans( order.transit_2 , Comission, self.__currency,
                                order.transit_1,  order, 
                                "comission", OutOrderId, False)

                     DebCred =   LiqPayTrans(
                                                  phone = Phone,
                                                  description = Desc,
                                                  #pib = ,
                                                  currency = self.__currency, 
                                                  amnt = Decimal(Amount) , 
                                                  user = order.user ,
                                                  comission = self.__comis,
                                                  user_accomplished_id =  1,
                                                  status = "processed",
                                                  debit_credit = "in",
                                                  confirm_key = Signature,
                                                  order = order
                                                 )
                     DebCred.save()
                     order.status = "processed"
                     order.save()
                     notify_email(order.user, "deposit_notify", DebCred ) 
                     Response =  HttpResponse( json.JSONEncoder().encode({"status":True,"signature":True}) )
                     Response['Content-Type'] = 'application/json'
                     return Response

           if Status == "sandbox":
                     raise TransError("hacker ")
                     order = Orders.objects.get(id = int(OrderId), status = "created")
                     order.status="processing"
                     order.save()
                     check_holds(order)

                     add_trans(order.transit_1, order.sum1, self.__currency,
                               order.transit_2, order, "payin", OutOrderId, False )
                     
                     
                     #Comission = order.sum1 * self.__comis
                     add_trans( order.transit_2, Comission , self.__currency,
                                order.transit_1,  order, 
                                "comission", OutOrderId, False)
                     DebCred =   LiqPayTrans(
                                                  phone = Phone,
                                                  description = Desc, 
                                                  currency = self.__currency, 
                                                  amnt = Decimal(Amount) , 
                                                  user = order.user ,
                                                  comission = self.__comis,
                                                  user_accomplished_id =  1,
                                                  status = "processed",
                                                  debit_credit = "in",
                                                  confirm_key = Signature,
                                                  order = order
                                                  
                                            )
                     DebCred.save()
                     order.status = "processed"
                     order.save()
                     Response =  HttpResponse( json.JSONEncoder().encode({"status":True,"signature":True}) )
                     Response['Content-Type'] = 'application/json'
                     return Response
           ##TODO add system message of some failure
           
                   


#Пример вызова API на Вашем сайте
#curl -v https://yoursite.com/callback \
  #-H "Accept: application/json" \
  #-d "public_key=i71547430402&" \
     #"amount=5&" \
     #"currency=UAH&" \
     #"description=Мой товар&" \
     #"type=buy&" \
     #"order_id=123456&" \
     #"status=success&" \        
     #"transaction_id=40011234&" \
     #"sender_phone=380951234567&" \
     #"signature=PHJlcXVlc3Q+PHZlcnNpb24+MS4yPC92ZXJ" 

#base64_encode( sha1( 
 #private_key+ 
 #amount+ 
 #currency+ 
 #public_key+ 
 #order_id+ 
 #type+ 
 #description+ 
 #status+ 
 #transaction_id + 
 #sender_phone 
#, 1 ));





#<form method="POST" action="https://www.liqpay.com/api/pay" accept-charset="utf-8">
  #<input type="hidden" name="public_key" value="i111111111111" />
  #<input type="hidden" name="amount" value="5" />
  #<input type="hidden" name="currency" value="UAH" />
  #<input type="hidden" name="description" value="Мой товар" />
  #<input type="hidden" name="order_id" value="123456" />
  #<input type="hidden" name="result_url" value="http://yoursite.com/return" />
  #<input type="hidden" name="server_url" value="https://yoursite.com/callback" />  
  #<input type="hidden" name="type" value="buy" />
  #<input type="hidden" name="signature" value="6aogGWpJar6EVQ6AKTktJClt8gw=" />
  #<input type="hidden" name="language" value="ru" />
  #<input type="hidden" name="sandbox" value="0" />
  #<input type="image" src="//static.liqpay.com/buttons/p1ru.radius.png" 
  #name="btn_text" />
#</form>
#base64_encode( sha1( 
 #private_key+ 
 #amount+ 
 #currency+ 
 #public_key+ 
 #order_id+ 
 #type+ 
 #description+ 
 #result_url+ 
 #server_url 
#, 1 ));
