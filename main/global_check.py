# -*- coding: utf-8 -*-

from main.models  import Accounts, Currency, TradePairs, sato2Dec
from blockchain.wallet import Wallet
from sdk.crypto import CryptoAccount
import crypton.settings
from sdk.crypto_settings import Settings as CryptoSettings
import json
import urllib2
'''
 <h3>Мы должны: {{item.currency}} <h3>
 <p>На ордерах: {{item.sum}} {{item.currency}} </p>
 <p>Ошибка: {{item.mistake}} {{item.currency}} </p>
 <p>Комиссия: {{item.comission}} {{item.currency}} </p>
 <p>Сальдо ввод - вывод: {{item.saldo}} </p> 
'''
import crypton.settings as settings
from django.db import connection
from decimal import Decimal
from sdk.p24 import p24


from main.models import VolatileConsts
def check_global_lock():
    try :
        l = list(VolatileConsts.objects.using("security").filter(Name = "global_lock"))
        return len(l)>2
    except :
        return False

def lock_global(Desc):
	lock = VolatileConsts(Name = "global_lock", Value = Desc)
	lock.save(using = "security")

def check_uah_balance():
        cursor = connection.cursor()
        cursor.execute("SELECT sum(balance) FROM main_accounts WHERE currency_id=1 AND balance>0 AND balance<1000000 AND id!=353 ");
        s = cursor.fetchone()*1
        if s == (None, ) :
              s = Decimal("0.0")
        else:
           (s, ) = s
        cursor.execute("SELECT sum(amnt)*0.99 FROM main_cardp2ptransfers WHERE status in ('created','processing','processing2','auto') AND pub_date>='2015-05-08' ");

        s1 = cursor.fetchone()*1
        if s1 == (None, ) :
              s1 = Decimal("0.0")
        else:
           (s1, ) = s1

        D = p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID2, settings.P24_PASSWD2, settings.P24MERCH_CARD2)
        D1 = p24("UAH", "https://api.privatbank.ua/", settings.P24_MERCHID, settings.P24_PASSWD, settings.P24MERCH_CARD)
        BalanceUAH  = Decimal(D.balance() ) + Decimal(D1.balance())
        return (BalanceUAH - s - s1)>0


def check_btc_balance():
        cursor = connection.cursor()
        cursor.execute("SELECT sum(balance) FROM main_accounts WHERE currency_id=2 AND balance>0 ");
        s = cursor.fetchone()*1
        if s == (None, ) :
              s = Decimal("0.0")
        else:
           (s, ) = s
        cursor.execute("SELECT sum(amnt) FROM main_cryptotransfers WHERE status in ('processing') AND currency_id=2 AND pub_date>='2015-05-08' " );

        s1 = cursor.fetchone()*1
        if s1 == (None, ) :
              s1 = Decimal("0.0")
        else:
           (s1, ) = s1

        Balance1  = 0 #
        Crypton = Wallet(CryptoSettings["BTC"]["host"],
                         CryptoSettings["BTC"]["rpc_user"],
                         CryptoSettings["BTC"]["rpc_pwd"])
        Balance2 = sato2Dec(Crypton.get_balance())
        print Balance2
        print Balance1
        print s
        print s1
        print Balance1+Balance2
        print s1+s	
        Delta = Balance1 + Balance2 - s - s1
        print "Delta is %s " % Delta
        return Delta>=0


def get_adress( Adr ):
    Url = "https://blockchain.info/address/%s?format=json" % (Adr)

    Decoder = json.JSONDecoder()
    D = urllib2.urlopen(Url)
    Str = D.read()
    Res = Decoder.decode(Str)
    return Res

def check_crypto_balance(Currency, Correction =  "0"):
        cursor = connection.cursor()
        cursor.execute("SELECT sum(balance) FROM main_accounts WHERE currency_id=%i AND balance>0" % Currency.id);
        s = cursor.fetchone()*1
        if s == (None, ) :
              s = Decimal("0.0")
        else:
           (s, ) = s

        cursor.execute("SELECT sum(amnt) FROM main_cryptotransfers WHERE status in ('processing') AND pub_date>='2015-05-08' and currency_id=%i " % Currency.id);

        s1 = cursor.fetchone()*1
        if s1 == (None, ) :
              s1 = Decimal("0.0")
        else:
           (s1, ) = s1
        Crypton = CryptoAccount(Currency.title, "trade_stock")
        Balance  = Crypton.getbalance()
        print "balance on wallet " + str(Balance)
        print s1+s
        Delta = (Decimal(Balance) - s1 - s + Decimal(Correction))
        print "Delta is %s " % Delta
        return Delta>0



def check_crypto_currency(Cur):
        
        Main_Account = Accounts.objects.get(user_id = settings.CRYPTO_USER, currency = Cur)
        cursor = connection.cursor()
        transit_accounts = []
        for pair  in TradePairs.objects.all():
            transit_accounts.append(str(pair.transit_on.id))
            transit_accounts.append(str(pair.transit_from.id))
        
        ComisId = settings.COMISSION_USER
        
        NotId = ",".join(transit_accounts)
        #not Credit and not Mistake and not transit accounts
        Query =  "SELECT sum(balance) FROM main_accounts \
                    WHERE currency_id=%s \
                    AND user_id not in (346, 31, %s) AND id not in (%s) AND balance>0 " % (str(Cur.id), ComisId, NotId)
                    
        cursor.execute(Query, [])
        S1 = cursor.fetchone()
        if S1 == (None, ) :
                S1 = Decimal("0.0")
        else :
                S1 = S1[0]
                
        Query = "SELECT sum(sum1) FROM main_orders \
                        WHERE currency1_id=%s AND currency2_id!=currency1_id \
                        AND status=\"processing\"  \
                        AND user_id not in (346)  " % (str(Cur.id))   
                        
        cursor.execute(Query, [  ])
        
        S2 = cursor.fetchone()*1
        if S2 == (None, ) :
                S2 = Decimal("0.0")
        else :
                S2 = S2[0]
        print S1
        print S2
        CheckSum  = S1 + S2
        print "balance in system "
        print CheckSum
        print "balance on wallet"
        print Main_Account.balance
        print "div between two sums "
        print CheckSum + Main_Account.balance
        if CheckSum <= abs(Main_Account.balance):
            return check_currency_orders(Cur)
        else :
            return True	


def check_currency_orders(Cur):
    
        cursor = connection.cursor()
        transit_accounts = []
        trade_pairs = []
        for pair  in TradePairs.objects.filter(status = "processing", currency_on = Cur):
            transit_accounts.append( str( pair.transit_on.id ) )
            trade_pairs.append( str( pair.id ) )

            
        for pair  in TradePairs.objects.filter(status = "processing", currency_from = Cur):
            transit_accounts.append( str( pair.transit_from.id ) )
            trade_pairs.append( str( pair.id ) )

            
        ComisId =  settings.COMISSION_USER
        InId = ",".join(transit_accounts)
        TradesId = ",".join(trade_pairs)
        Query = "SELECT sum(balance) FROM main_accounts WHERE  id IN (%s)  " % (InId)
        cursor.execute(Query, [])
            
        TransitSum = cursor.fetchone()*1
        if TransitSum == (None, ) :
                TransitSum = Decimal("0.0")
        else :
                TransitSum = TransitSum[0]  
        Query = "SELECT sum(sum1) FROM main_orders \
                        WHERE currency1_id=%s AND currency2_id!=currency1_id \
                        AND status=\"processing\"  \
                        AND user_id not in (346)  " % ( str(Cur.id) )        
        cursor.execute(Query, [])
        
        OrdersSum = cursor.fetchone()*1
        if OrdersSum == (None, ) :
                OrdersSum = Decimal("0.0")
        else :
                OrdersSum = OrdersSum[0]
                
        print OrdersSum
        print TransitSum
    
        if TransitSum <= OrdersSum  :
            return True
        else :
            if TransitSum - OrdersSum > 0.1 :
                return False
            else :
                return True

		

def check_fiat_currency(Cur):
        cursor = connection.cursor()
        pay_in_out = []
        for pair  in TradePairs.objects.filter( currency_on = Cur, currency_from  = Cur):
            pay_in_out.append(str(pair.transit_on.id))
            pay_in_out.append(str(pair.transit_from.id))
            
        ComisId =  settings.COMISSION_USER
        MainIn = ",".join(pay_in_out)
        Query = "SELECT sum(balance) FROM main_accounts WHERE  in (%s) " % (MainIn)
        #not Credit and not Mistake and not transit accounts
        cursor.execute(Query, [])
            
        WholeSum = cursor.fetchone()*1
        if  WholeSum == (None, ) :
                WholeSum = Decimal("0.0")
                
        transit_accounts = []
        for pair  in TradePairs.objects.all():
            transit_accounts.append(str(pair.transit_on.id))
            transit_accounts.append(str(pair.transit_from.id))
            
        ComisId =  settings.COMISSION_USER
        NotId = ",".join(transit_accounts)
        #not Credit and not Mistake and not transit accounts
        Query = "SELECT sum(balance) FROM main_accounts WHERE currency_id=%s \
                            AND user_id not in (346, 31) AND id not in (%s) AND balance>0 " % (str(Cur.id), NotId)
        cursor.execute(Query, [])
            
        S1 = cursor.fetchone()*1
        if S1 == (None, ) :
                S1 = Decimal("0.0")
        
        Query = "SELECT sum(sum1) FROM main_orders WHERE currency1_id=%s AND currency2_id!=currency1_id \
                                                AND status=\"processing\"  \
                            AND user_id not in (346)  " % ( str(Cur.id) )
        cursor.execute(Query, [])
        
        S2 = cursor.fetchone()*1
        if S2 == (None, ) :
                S2 = Decimal("0.0")
        print S1
        print S2
        print Main_Account.balance
        if S1 + S2 < WholeSum:
            return check_currency_orders(Cur)
        else :
            return True 
        
        
        
