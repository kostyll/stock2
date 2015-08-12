from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from django.db import connection
from main.models import Orders, process_p24_in, cancel_p24_in, TradePairs

class Command(BaseCommand):
    args = ''
    help = 'fix user currency'
    def handle(self, *args, **options):
        from sdk.p24 import p24
        TradePair = TradePairs.objects.get(url_title = "p24")
        D = p24()        
        for item in  Orders.objects.filter(trade_pair = TradePair, status="wait_secure"):
                Res = D.check_payment(item.id, True)
                item.status = "processing2"
                item.save()
                if Res == 1 :
                    process_p24_in(item.id, D.description, D.comis )    
                    
                if Res == 0:
                    cancel_p24_in(item.id)    
                        
                    
        for item in  Orders.objects.filter(trade_pair = TradePair, status="processing"):
                Res = D.check_payment(item.id, True)
                item.status = "processing2"
                item.save()
                if Res == 1:
                    process_p24_in(item.id, D.description, D.comis ) 
                    
                if Res == 0:
                    cancel_p24_in(item.id)
                    
       
