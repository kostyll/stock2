from django.core.management.base import BaseCommand, CommandError
from main.models import TradePairs, VolatileConsts, dictfetchall
from datetime import datetime
from django.db import connection
from main.api import format_numbers10,format_numbers, format_numbers_strong


class Command(BaseCommand):
    args = ''
    help = 'update top prices'
    def handle(self, *args, **options):
                cursor = connection.cursor()
                for item in  TradePairs.objects.filter(status = "processing"):
                        Query =  cursor.execute("SELECT  min(main_orders.price) as top_price \n\
                                                  FROM  main_orders, main_tradepairs\n\
                                                  WHERE main_orders.status='processing'\n\
                                                  AND main_orders.trade_pair_id = %i \n\
                                                  AND  main_tradepairs.id = %i \n\
                                                  AND main_orders.currency1_id =  main_tradepairs.currency_on_id \n\
                                                  \n\
                                                 " % ( item.id, item.id ))
                        List = dictfetchall(cursor, Query)
                        CurrentName  = item.url_title + "_top_price"
                        CurrentPrice = None
                        try :
                               CurrentPrice  = VolatileConsts.objects.get(Name = CurrentName)
                        except :
                               CurrentPrice  = VolatileConsts(Name = CurrentName, 
                                                             Value = "None" )
                               CurrentPrice.save()
                               
                        if List[0]["top_price"] is not None and List[0]["top_price"]>0:
                                top_price = List[0]["top_price"] 
                                print top_price
                                
                                if top_price>=0.1:
                                        CurrentPrice.Value =  format_numbers(top_price)
                                        
                                if top_price<0.1 and top_price > 0.001:
                                        CurrentPrice.Value =  format_numbers(top_price)        
                                        
                                if top_price<0.00001 :
                                        CurrentPrice.Value =  format_numbers10(top_price)        
                                print " to "
                                print CurrentPrice.Value
                                
                                CurrentPrice.save()
                        else:
                                CurrentPrice.Value = "No deals" 
                                CurrentPrice.save()
                                

       
       