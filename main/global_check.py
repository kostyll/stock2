# -*- coding: utf-8 -*-

from main.models  import Accounts, Currency, TradePairs


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
                        AND user_id not in (346)  " % ( str(Cur.id))
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
        
        
        