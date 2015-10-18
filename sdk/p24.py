# -*- coding: utf-8 -*-

from crypton import settings

from base64 import b64encode
import hashlib 
from decimal import Decimal
from main.models import Accounts, TradePairs, Orders, Currency, TransError, process_p24_in
from django.contrib.auth.models import User
import urllib2
import urllib
from django.http import HttpResponse 
import json
from xml.dom import minidom


class p24:
        
    @staticmethod          
    def str_class_name():
        return     "p24"

    def get_traid_pair(self):
            return  self.__trade_pair

#public_key      
#private_key    
    
    
    def __init__(self,   Cur = "UAH", api_url = "https://api.privatbank.ua/", 
                    public_id =  settings.P24_MERCHID,
                    password = settings.P24_PASSWD,
                    card_acc = settings.P24MERCH_CARD,
                    phone = "380973426645"
            ):
        self.__public_id = public_id
        self.__password = password
        self.__my_orderid = "1"
        self.__min_amnt = Decimal("100.00")
        self.comis = Decimal("0.02")
        self.__phone = phone 
        self.__card = card_acc
        self.description = "buying_btc"
        P24User =  User.objects.get(username = p24.str_class_name() )        
        CurrencyPay =  Currency.objects.get( title = Cur)        
        self.__currency = CurrencyPay
        self.__transit_account = Accounts.objects.get(user  = P24User, currency = CurrencyPay)
        self.__trade_pair = TradePairs.objects.get(transit_on = self.__transit_account,
                                                   transit_from  = self.__transit_account )
        self.__api_url = api_url
       
    
    def records(self, FromYear, FromMonth ):
          url = self.__api_url + "p24api/rest_yur"
          Data = "<oper>cmt</oper><wait>10</wait><test>0</test><payment id=\"\" ><prop name=\"year\" value=\"%s\" /><prop name=\"month\" value=\"%s\" /></payment>\"" % (FromYear, FromMonth)
          signature = self.signature(Data)
          PrePostData = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> <request version=\"1.0\">\
<merchant><id>%s</id>\
<signature>%s</signature>\
</merchant><data>%s</data>\
</request>" % (self.__public_id, signature, Data )
                   
          #$sign=encode_base64(sha1($merch_sign.$xml.$merch_sign));
          
# Send HTTP POST request
          headers = {'User-Agent' : 'Mozilla 5.10', 'Content-Type': 'text/xml'}
          request = urllib2.Request(Url, PrePostData, headers)

          response = urllib2.urlopen(request)
          xml = response.read()
          doc = minidom.parseString(xml)
          print xml
          Data = xml.split("<data>")[1].split("</data>")[0]  
          CalcSign = self.signature(Data)
          if CalcSign != Sign :
                  raise TransError("Invalid Signature %s calculated %s" % (CalcSign, Sign) )
          
          return Decimal(Balance)    
    
    def generate_button(self, Amnt):
           Data =  "<form method=\"POST\" id=\"pay_p24_form\" action=\"https://api.privatbank.ua/p24api/ishop\">\n\
<input type=\"hidden\"  id=\"p24_amt\" name=\"amt\" value=\"%s\" />\n\
<input type=\"hidden\"  id=\"p24_ccy\" name=\"ccy\" value=\"UAH\" />\n\
<input type=\"hidden\"  id=\"p24_public_key\" name=\"merchant\" value=\"%s\" />\n\
<input type=\"hidden\"  id=\"p24_order_id\" name=\"order\" value=\"\" />\n\
<input type=\"hidden\"  id=\"p24_description\" name=\"details\" value=\"\" />\n\
<input type=\"hidden\"  id=\"p24_ext_details\" name=\"ext_details\" value=\"\" />\n\
<input type=\"hidden\"  id=\"p24_type\" name=\"pay_way\" value=\"privat24\" />\n\
<input type=\"hidden\"  id=\"p24_return_url\" name=\"return_url\" value=\"https://www.btc-trade.com.ua/finance/p24/deposit/hui1\" />\n\
<input type=\"hidden\"  id=\"p24_server_url\" name=\"server_url\" value=\"https://www.btc-trade.com.ua/finance/p24/hui_hui_hui/1231\" />\n\
<button type=\"submit\" id=\"p24_submit_button\"><img src=\"https://static.liqpay.com/buttons/p1ru.radius.png\" border=\"0\" /></button>\n\
</form>" % (Amnt, self.__public_id)
           return Data
       
    def   balance(self, verbose = True):
          Url = self.__api_url + "p24api/balance"
          Data = "<oper>cmt</oper><wait>10</wait><test>0</test><payment id=\"\" ><prop name=\"cardnum\" value=\"%s\" /><prop name=\"country\" value=\"UA\" /></payment>\"" % (self.__card)
          
          signature = self.signature(Data)
          PrePostData = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> <request version=\"1.0\">\
<merchant><id>%s</id>\
<signature>%s</signature>\
</merchant><data>%s</data>\
</request>" % (self.__public_id, signature, Data )
                   
          #$sign=encode_base64(sha1($merch_sign.$xml.$merch_sign));
          
# Send HTTP POST request
          headers = {'User-Agent' : 'Mozilla 5.10', 'Content-Type': 'text/xml'}
          request = urllib2.Request(Url, PrePostData, headers)

          response = urllib2.urlopen(request)
          xml = response.read()
<<<<<<< HEAD
=======
	  if verbose:	
		print xml
>>>>>>> 137e852afcc19395c1c41f4212fde52f31cbc0a7
          doc = minidom.parseString(xml)
          Sign = doc.getElementsByTagName("signature")[0].childNodes[0].nodeValue               
          Balance = doc.getElementsByTagName("balance")[0].childNodes[0].nodeValue
          Data = xml.split("<data>")[1].split("</data>")[0]  
          CalcSign = self.signature(Data)
          if CalcSign != Sign :
                  raise TransError("Invalid Signature %s calculated %s" % (CalcSign, Sign) )
          
          return Decimal(Balance)
          
         

          
    def pay2p(self, OrderId, ToCard, Amnt):
          self.__my_orderid = str(OrderId)
	 
          Data = "<oper>cmt</oper><wait>10</wait>\
<test>0</test><payment id=\"%s\"><prop name=\"b_card_or_acc\" value=\"%s\" />\
<prop name=\"ccy\" value=\"%s\" />\
<prop name=\"amt\" value=\"%s\" />\
<prop name=\"phone\" value=\"%s\" />\
<prop name=\"details\" value=\"%s\" />\
</payment>" % (self.__my_orderid,
                      ToCard, 
                      self.__currency.title,
                      Amnt, 
                      self.__phone,
                      self.description)
          
          signature = self.signature(Data)
          PrePostData = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> <request version=\"1.0\">\
                   <merchant><id>%s</id>\
                   <signature>%s</signature>\
                   </merchant><data>%s</data>\
                   </request>" % (self.__public_id, signature, Data )
                   
          #$sign=encode_base64(sha1($merch_sign.$xml.$merch_sign));
          
# Send HTTP POST request
          headers = {'User-Agent' : 'Mozilla 5.10', 'Content-Type': 'text/xml'}
          request = urllib2.Request(self.__api_url + "p24api/pay_pb", PrePostData, headers)

          response = urllib2.urlopen(request)
 
          xml = response.read()
          doc = minidom.parseString(xml)
          Sign = doc.getElementsByTagName("signature")[0].childNodes[0].nodeValue
          
          
          Payment = doc.getElementsByTagName("payment")[0]
          Data = xml.split("<data>")[1].split("</data>")[0]          
          
          CalcSign = self.signature(Data)
          if CalcSign != Sign :
                  raise TransError("Invalid Signature %s calculated %s" % (CalcSign, Sign) )
          
          if Payment.getAttribute("state")== "1":
                return True
          
          raise TransError("Invalid State %s " % (xml) )
          
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
          
    def signature(self, Data):
            #return hashlib.sha1( hashlib.md5(Data + self.__password).hexdigest() ).hexdigest()
	    Str = u''.join((Data, self.__password)).encode('utf-8').strip()
            return hashlib.sha1( hashlib.md5(Str).hexdigest() ).hexdigest()
    def generate_pay_request(self, User, Amount):
        AmountStr = Decimal(Amount)    
        user_account = Accounts.objects.get(user  = User, currency = self.__currency)
        if AmountStr<0:
                raise TransError("NegativeAmount")
        
        if AmountStr < self.__min_amnt  :
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
                                status = "processing"
                        )
        order.save()
        ResultUrl = self.generate_result_url(order, User,  Amount )
        ServerResultUrl = self.generate_api_result_url(order, User,  Amount )
        #
        Payment="amt=%s&ccy=%s&details=%s&ext_details=%s&pay_way=privat24&order=%s&merchant=%s" % (str(AmountStr), 
                                                                                                       self.__currency.title,
                                                                                                       self.description,
                                                                                                       "none",
                                                                                                       str(order.id),
                                                                                                       self.__public_id
                                                                                                       )
        signature = self.signature(Payment)
        Dict = {
                "signature":signature,
                "public_key": self.__public_id,
                "order_id":   str(order.id),
                "result_url" : ResultUrl,
                "type":"privat24",
                "ext_details":"none",
                "description" :self.description,
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
            return settings.BASE_URL + "finance/p24/hui_hui_hui/"+str(order.id)
    
    
    def check_payment(self, OrderId, verbose = False):
          self.__my_orderid = str(OrderId)
          #<?xml version="1.0" encoding="UTF-8"?> 
          #<request version="1.0"> 
          #<merchant>    <id>99137</id>  
          #<signature>b45d66d192cb258ba1661a978e08cfe1ca171535</signature>
          #</merchant>
          #<data>   <oper>cmt</oper>   <wait>0</wait>    <test>0</test>    <payment>
          #<prop name="order" value="PAY-15893" />    </payment> </data> </request>
          
          
          Data = "<oper>cmt</oper><wait>10</wait><test>0</test><payment><prop name=\"order\" value=\"%s\" /></payment>"  % ( self.__my_orderid )
          
          signature = self.signature(Data)
          PrePostData = "<?xml version=\"1.0\" encoding=\"UTF-8\"?> <request version=\"1.0\">\
                   <merchant><id>%s</id>\
                   <signature>%s</signature>\
                   </merchant><data>%s</data>\
                   </request>" % (self.__public_id, signature, Data )
                   
          if verbose :
                print " send data"
                print PrePostData
          #$sign=encode_base64(sha1($merch_sign.$xml.$merch_sign));
          
# Send HTTP POST request
          headers = {'User-Agent' : 'Mozilla 5.10', 'Content-Type': 'text/xml'}
          request = urllib2.Request(self.__api_url + "p24api/ishop_pstatus", PrePostData, headers)
          response = urllib2.urlopen(request)
        #<payment order="PAY-15893" state="not found" /> 
          xml = response.read()
          if verbose :
                  print xml
          doc = minidom.parseString(xml)
          Sign = doc.getElementsByTagName("signature")[0].childNodes[0].nodeValue
          Payment =   doc.getElementsByTagName("payment")[0].getAttribute("state")
          Data = xml.split("<data>")[1].split("</data>")[0]
          if verbose :
                print "calc data"  
                print "'%s' " % (Data)
          CalcSign = self.signature(Data)

          if CalcSign != Sign :
                  raise TransError("Invalid Signature %s calculated %s" % (CalcSign, Sign) )
          
          if Payment == "ok":
                return 1
          if Payment == "fail":
                return 0
          if Payment == "not found" :
                return 0  
          return -1
          
          
    def api_callback_pay(self, Params, OrderId):
            
            
            
           Payment = Params["payment"] 
           signature = self.signature(Payment)
           Signature =  Params["signature"]
           #if signature != Signature: 
                    #raise TransError("Invalid Signature")           
           
           for Val in Payment.split("&"):
             [Name, Value] =  Val.split("=")  
             if Name == "state":
                    Status = Value 
                    break
            
              
           if Status == "fail":
                     order = Orders.objects.get( id = int(OrderId) )
                     order.status = "order_cancel"
                     order.save()
                     Response =  HttpResponse( json.JSONEncoder().encode({"status":True,"signature":True}) )
                     Response['Content-Type'] = 'application/json'
                     return Response
             
           if Status == "wait":
                     Response =  HttpResponse( json.JSONEncoder().encode({"status":True,"signature":True}) )
                     Response['Content-Type'] = 'application/json'
                     return Response
             
           ##TODO add system message  
           if Status == "ok":
                     process_p24_in(int(OrderId), self.description, self.comis, self.__password)
                     Response =  HttpResponse( json.JSONEncoder().encode({"status":True,"signature":True}) )
                     Response['Content-Type'] = 'application/json'
                     return Response

           if Status == "test":
                     order = Orders.objects.get(id = int(OrderId), status = "created")
                     order.status="processing"
                     order.save()
                     add_trans(order.transit_1, order.sum1, self.__currency,
                               order.transit_2, order, "payin", OutOrderId, False )
                     Comission = order.sum1 * self.comis
                     add_trans( order.transit_2, Comission , self.__currency,
                                order.transit_1,  order, 
                                "comission", OutOrderId, False)
                     DebCred =   P24TransIn(
                                                  description = self.description, 
                                                  currency = self.__currency, 
                                                  amnt = order.sum1 , 
                                                  user = order.user ,
                                                  comission = Comission,
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
          
        




