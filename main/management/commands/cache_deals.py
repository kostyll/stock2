# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from main.models import TradePairs, DealsMemory, OrdersMem, dictfetchall, TransMem
from main.http_common import format_numbers10
from datetime import date
from django.db import connection


class Command(BaseCommand):
    args = ''
    help = 'move memory orders to disk'
    def handle(self, *args, **options):
        cursor = connection.cursor()
        
        for Market  in TradePairs.objects.filter(status = "processing"):
      
            Query =  cursor.execute("SELECT  main_transmem.amnt as amnt,\
                                         main_transmem.pub_date as ts,\
                                         price,  \
                                         main_transmem.currency_id as currency_id, \
                                         username  as username, \
                                         main_transmem.user2_id as trans_owner_id, \
                                         main_ordersmem.user as order_owner_id, \
                                         main_ordersmem.sum1_history as order_sum1,\
                                         main_ordersmem.sum2_history as order_sum2 \
                                         FROM main_transmem, main_ordersmem,\
                                              main_accounts, auth_user \
                                         WHERE \
                                         main_ordersmem.trade_pair = %i \
                                         AND main_ordersmem.id = main_transmem.order_id  \
                                         AND main_accounts.id = main_transmem.user2_id \
                                         AND auth_user.id = main_accounts.user_id \
                                         AND main_transmem.status='deal' \
                                         ORDER BY main_transmem.pub_date " % ( Market.id))
            List = dictfetchall(cursor, Query)
            ResList = []
            for item in  List :
                new_item  = process_deal_item( item, Market )
                ResList.append(new_item)
            DealsMemory.objects.bulk_create(ResList)
            
        for item in OrdersMem.objects.filter(status="processed"):
            ArchiveOrder = item.stable_order(str(item.user))
            for trans in TransMem.objects.filter(order_id = item.id ).order_by('id'):
                trans.archive(ArchiveOrder)
            item.delete()
        
        for item in OrdersMem.objects.filter(status="canceled").order_by('id'):
            ArchiveOrder = item.stable_order(str(item.user))
            for trans in TransMem.objects.filter(order_id = item.id ).order_by('id'):
                trans.archive(ArchiveOrder)
            item.delete()
        
        
       
        
        

def process_deal_item(item, Current):          
    new_item = {}
    new_item['user_id'] = int(item["trans_owner_id"])
    if  int(item["trans_owner_id"]) != int(item["order_owner_id"]) :         
            
            
        rate = item["price"]
        if int(item["currency_id"]) == int(Current.currency_on.id) : 
                new_item["type"] = "buy"
                new_item["user"] = item["username"]
                new_item["price"] = format_numbers10(rate)
                new_item["amnt_base"] = format_numbers10(item["amnt"]*rate)
                new_item["amnt_trade"] = format_numbers10(item["amnt"])     
                        
        else :
                new_item["type"] = "sell"
                new_item["user"] = item["username"]
                new_item["price"] = format_numbers10(rate)
                new_item["amnt_base"] = format_numbers10(item["amnt"])
                new_item["amnt_trade"] = str(item["amnt"]/rate)
                
                
    else :
        rate = item["price"]
        if int(item["currency_id"]) == int(Current.currency_on.id) : 
                new_item["type"] = "buy"
                new_item["user"] = item["username"]
                new_item["price"] = format_numbers10(rate)
                new_item["amnt_base"] = format_numbers10(item["amnt"]/rate)
                new_item["amnt_trade"] = format_numbers10(item["amnt"])     
                        
        else :
                new_item["type"] = "sell"
                new_item["user"] = item["username"]
                new_item["price"] = format_numbers10(rate)
                new_item["amnt_base"] = format_numbers10(item["amnt"])
                new_item["amnt_trade"] = format_numbers10(item["amnt"]*rate) 
                
                
    return DealsMemory(type_deal=new_item["type"],
                       user=new_item["user"],
                       amnt_base=new_item["amnt_base"],
                       amnt_trade=new_item["amnt_trade"],
                       price=new_item["price"],
                       pub_date=item["ts"],
                       trade_pair=Current.id,
                       user_id=new_item['user_id'] 
                       )    
        
                                

       
       
