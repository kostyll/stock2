from django.core.management.base import BaseCommand, CommandError
from main.models import StockStat, Orders, dictfetchall,TradePairs
from django.db import connection
from datetime import datetime
from decimal import getcontext


def get_current_range(Now):
    if (Now.minute>30 and Now.minute<=59  ):
            D1 = datetime(Now.year, Now.month, Now.day, Now.hour, 30, 0)
            D2 = datetime(Now.year, Now.month, Now.day, Now.hour, 59, 59)
            return (D1, D2)
    
    if (Now.minute>=0 and Now.minute<=30):
            D1 = datetime(Now.year, Now.month, Now.day, Now.hour, 0, 0)
            D2 = datetime(Now.year, Now.month, Now.day, Now.hour, 31, 0)
            return (D1, D2)
        


class Command(BaseCommand):
  args = '<Stock Title ...>'
  help = 'every minute get stock prices and save it to StockStat'

  def handle(self, *args, **options):
      print "stock_stat"
      print "=============================="  
      getcontext().prec = 6
      cursor = connection.cursor()
        
      Now  = datetime.now()
      (Range1, Range2) =  get_current_range(Now);
      for Market in  TradePairs.objects.filter( status = "processing") :
         
            StockStatistic  = None 
            try :
                    StockStatistic = StockStat.objects.get(Status = "current", Stock = Market)
            except :
        
                StockStatisticaPast = StockStat.objects.filter( Status = "past",  Stock = Market).latest('id')
                    
                StockStatistic = StockStat(
                                            start_date = Range1, 
                                            end_date = Range2,
                                            Start = StockStatisticaPast.End ,
                                            End = StockStatisticaPast.End ,
                                            Min = StockStatisticaPast.End,
                                            Max = StockStatisticaPast.End,
                                            Stock = Market,
                                            VolumeBase = 0,
                                            VolumeTrade = 0,
                                            Status = "current"
                                    )
                StockStatistic.save()
                #continue
                
                
                
            CurrentStockStat = None
            if StockStatistic.start_date < Now and  StockStatistic.end_date > Now:
                CurrentStockStat = StockStatistic
                self.stdout.write('Use previos window ' ) 

            else:
                StockStatistic.Status = "past"
                StockStatistic.save()
                self.stdout.write('Start new window ' ) 

                CurrentStockStat = StockStat(
                                            start_date = Range1, 
                                            end_date = Range2,
                                            Start = StockStatistic.End ,
                                            End = StockStatistic.End ,
                                            Min = StockStatistic.End,
                                            Max = StockStatistic.End,
                                            Stock = Market,
                                            VolumeBase = 0,
                                            VolumeTrade = 0,
                                            Status = "current"
                                            )
        
            OrdersList  = Orders.objects.filter(trade_pair = Market, status = "processing")
            self.stdout.write('get orders ' )
            
            Query =  cursor.execute("SELECT  main_trans.amnt as amnt,\
                                            main_trans.pub_date as ts,\
                                            price,  \
                                            main_trans.currency_id as currency_id, \
                                            username  as username, \
                                            main_trans.user2_id as trans_owner_id, \
                                            main_orders.user_id as order_owner_id, \
                                            main_orders.sum1_history as order_sum1,\
                                            main_orders.sum2_history as order_sum2 \
                                            FROM main_trans, main_orders, main_accounts, auth_user \
                                            WHERE \
                                            main_orders.trade_pair_id = %i \
                                            AND main_orders.id = main_trans.order_id  \
                                            AND main_accounts.id = main_trans.user2_id \
                                            AND auth_user.id = main_accounts.user_id \
                                            AND main_trans.status='deal' \
                                            AND  (main_trans.pub_date>'%s'   AND  main_trans.pub_date<'%s') \
                                            ORDER BY main_trans.pub_date DESC LIMIT 100" %
                                            ( Market.id, 
                                            str(Range1),
                                            str(Range2) ) 
                                            
                                            )
        
        #Query =  cursor.execute("SELECT  main_trans.amnt as amnt,\
                                         #main_trans.pub_date as ts,\
                                         #currency_id, \
                                         #main_orders.sum1_history as order_sum1,\
                                         #main_orders.sum2_history as order_sum2 \
                                         #FROM main_trans, main_orders \
                                         #WHERE \
                                         #main_orders.trade_pair_id = %i \
                                         #AND  (main_trans.pub_date>'%s'   AND  main_trans.pub_date<'%s') \
                                         #AND main_orders.id = main_trans.order_id  AND main_trans.status='deal'\
                                         #ORDER BY main_trans.id \
                                         #" %
                                         #( Market.id, 
                                           #str(Range1),
                                           #str(Range2) ) 
                               #)
            self.stdout.write('get transactions ' )
            List = dictfetchall(cursor, Query)
            ResList = []
            self.stdout.write(' init params ' )
            
            EndRate = CurrentStockStat.End
            self.stdout.write('end rate ' )

            VolumeTrade = 0
            VolumeBase = 0
            TradeCurrencyId =  int(Market.currency_on.id)
            MaxRate =  0 # CurrentStockStat.Max
            MinRate = CurrentStockStat.Min
        
###process Deals 
        
            for item in  List :
                self.stdout.write('Successfully closed poll "%s"' % (item["amnt"]) ) 
                if  int(item["currency_id"]) ==  TradeCurrencyId: 
                    self.stdout.write('adding valume from') 
                    VolumeTrade =   VolumeTrade + item["amnt"]  
                    rate = item["price"]
                else:   
                    self.stdout.write('adding valume base' )
                    VolumeBase =  VolumeBase + item["amnt"]  
                    rate = item["price"]
                
                if rate < MinRate :
                    MinRate = rate
                    
                if rate > MaxRate :
                    MaxRate = rate 
                    
                EndRate = rate    
            
            if MaxRate == 0:
                    MaxRate = CurrentStockStat.Max
                    
            if MinRate == 0 :        
                    MinRate = CurrentStockStat.Min
            
            CurrentStockStat.VolumeBase =  VolumeBase      
            CurrentStockStat.VolumeTrade = VolumeTrade           
            CurrentStockStat.End = EndRate
            CurrentStockStat.Min = MinRate      
            CurrentStockStat.Max = MaxRate          
            CurrentStockStat.save()
       
       
